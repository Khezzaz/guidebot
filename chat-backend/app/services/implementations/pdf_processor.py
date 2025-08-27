# app/services/implementations/processors/pdf_processor.py
import os
import re
import uuid
import datetime
from typing import List, Tuple
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from llama_index.core import Document
from llama_index.core.settings import Settings
from llama_index.core.node_parser.text.semantic_splitter import SemanticSplitterNodeParser

from app.core.embedding import embed_model
from app.models.qdrant_dto import QdrantDocumentInput
from app.models.pdf_metadata import PDFMetadata
from app.services.utils.idsFactory import IdsFactory

Settings.embed_model = embed_model
Settings.llm = None

UPLOAD_DIR = "app/documents/uploaded"

class PdfProcessor:
    def __init__(self):
        self.upload_dir = UPLOAD_DIR
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)
    
    def save_uploaded_pdf(self, file: UploadFile) -> str:
        """Sauvegarde le fichier PDF uploadé et retourne son chemin absolu."""
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        return file_path
    
    def extract_full_text(self, file_path: str) -> str:
        """Charge le PDF, concatène toutes les pages, et renvoie le texte."""
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        raw = "\n".join(page.page_content for page in pages)
        return raw
    
    def clean_text(self, text: str) -> str:
        """Nettoyage du texte extrait."""
        # Supprime les en‑têtes/pieds de page du type "Page 1 / 10"
        text = re.sub(r"\s*Page\s+\d+\s*/\s*\d+\s*", " ", text, flags=re.IGNORECASE)
        # Réduit les espaces multiples
        text = re.sub(r"\s{2,}", " ", text)
        # Élimine les lignes vides
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)
    
    async def vectorize_text(self, text: str, file_name: str, system_name: str) -> Tuple[List[QdrantDocumentInput], PDFMetadata]:
        """Vectorise le texte en chunks sémantiques."""
        # 1. Chunking sémantique
        parser = SemanticSplitterNodeParser.from_defaults(embed_model=embed_model)
        seed_doc = Document(text=text, metadata={"source_file": file_name})
        nodes = parser.get_nodes_from_documents([seed_doc])
        
        # 2. Générer les IDs
        ids_factory = IdsFactory(text)
        created_at = datetime.datetime.utcnow().isoformat()
        
        # 3. Embedding + Structuration
        qdrant_inputs: List[QdrantDocumentInput] = []
        for i, node in enumerate(nodes):
            embedding = embed_model.get_text_embedding(node.text)
            chunk_id = ids_factory.create_chunk_id(i)
            
            metadata = {
                "chunk_id": chunk_id,
                "chunk_index": i,
                "created_at": created_at,
                "system_name": system_name,
                "filename": file_name,
                "doc_hash": ids_factory.get_pdf_hash()
            }
            
            qdrant_inputs.append(QdrantDocumentInput(
                id=chunk_id,
                content=node.text,
                metadata=metadata,
                embedding=embedding
            ))
        
        # 4. Créer les métadonnées PDF
        pdf_metadata = PDFMetadata(
            filename=file_name,
            file_hash=ids_factory.get_pdf_hash(),
            created_at=created_at,
            system_name=system_name
        )
        
        return qdrant_inputs, pdf_metadata