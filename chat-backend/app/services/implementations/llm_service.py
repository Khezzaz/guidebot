from typing import List, Dict
import logging
from huggingface_hub import InferenceClient

from app.services.interfaces.llm_interface import LlmInterface
from app.core.config import HF_TOKEN

logger = logging.getLogger(__name__)

class MistralLlmService(LlmInterface):
    def __init__(self):
        self.model_name = "openai/gpt-oss-20b"
        self.client = InferenceClient(
            provider="novita",
            api_key=HF_TOKEN
        )

    def query_with_context(self, question: str, retrieved_chunks: List[str]) -> str:
        """
        Génère un guide pas à pas basé sur les documents fournis.
        """
        try:
            # Construction du contexte
            context_text = "\n\n".join(
                f"[Document {i}]\n{chunk}"
                for i, chunk in enumerate(retrieved_chunks, start=1)
            )

            # Prompt système 
            system_prompt = (
                "Tu es un assistant expert chargé de créer des guides pas à pas. "
                "Tu DOIS répondre EXCLUSIVEMENT en français. "
                "Fournis des réponses sous forme d'un guide clair, structuré en étapes numérotées. "
                "Ne montre jamais tes étapes de réflexion ou calcul, donne uniquement le guide final. "
                "Utilise uniquement les informations fournies ; si elles sont absentes, indique « Information non trouvée dans les documents fournis »."
            )

            user_message = f"Contexte (documents fournis) :\n{context_text}\n\nQuestion : {question}"

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]

            # Appel LLM 
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=4000,       
                temperature=0.7,        
                top_p=0.95
            )

            return completion.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Erreur lors de l'inférence LLM: {str(e)}")
            return f"Erreur lors de l'inférence : {e}"

    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Génère une réponse libre pour un prompt donné.
        """
        try:
            messages = [{"role": "user", "content": prompt}]

            # Permet de laisser le modèle libre tout en gardant des valeurs par défaut sûres
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=kwargs.get('max_tokens', 4000),
                temperature=kwargs.get('temperature', 1.0),  
                top_p=kwargs.get('top_p', 0.95)
            )

            return completion.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse: {str(e)}")
            return f"Erreur lors de la génération : {e}"