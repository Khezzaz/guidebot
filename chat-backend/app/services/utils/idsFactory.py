import hashlib
import uuid

class IdsFactory:
    def __init__(self, pdf_content: str):
        """
        Initialise l'IdsFactory avec le contenu brut du PDF.

        :param pdf_content: Contenu textuel du PDF.
        """
        self.pdf_content = pdf_content
        self._pdf_hash = self._compute_pdf_hash()

    def _compute_pdf_hash(self) -> str:
        """
        Calcule et retourne le hash SHA-256 du contenu du PDF.

        :return: Hash en hexadécimal.
        """
        return hashlib.sha256(self.pdf_content.encode("utf-8")).hexdigest()

    def get_pdf_hash(self) -> str:
        """
        Retourne le hash calculé du PDF.

        :return: Hash en hexadécimal.
        """
        return self._pdf_hash

    def create_chunk_id(self, chunk_index: int) -> str:
        """
        Crée un identifiant UUID unique pour un chunk basé sur le hash du PDF et l'index du chunk.

        :param chunk_index: Index du chunk dans le document.
        :return: UUID v5 (nommé) sous forme de chaîne.
        """
        raw_id = f"{self._pdf_hash}_{chunk_index}"
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, raw_id))  # UUID stable et unique
