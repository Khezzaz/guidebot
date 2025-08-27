# app/services/implementations/local_llm_service.py
from typing import List, Dict
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from app.services.interfaces.llm_interface import LlmInterface
from app.core.config import MODEL_HF_NAME, DEVICE  

logger = logging.getLogger(__name__)

class LocalLlmService(LlmInterface):
    """Service LLM local qui charge le modèle depuis Hugging Face Hub (Singleton)."""

    _instance = None
    _model = None
    _tokenizer = None
    _pipeline = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalLlmService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._load_model()

    def _load_model(self):
        """Charge le modèle directement depuis Hugging Face Hub et crée le pipeline."""
        try:
            logger.info(f"Chargement du modèle depuis Hugging Face Hub: {MODEL_HF_NAME}")
            logger.info(f"Device demandé: {DEVICE} | GPU disponible: {torch.cuda.is_available()}")

            tokenizer_kwargs = {"trust_remote_code": True}
            model_kwargs = {
                "trust_remote_code": True,
                "torch_dtype": torch.float16 if DEVICE == "cuda" and torch.cuda.is_available() else torch.float32,
                "low_cpu_mem_usage": True
            }

            # Tokenizer
            logger.info("Chargement du tokenizer...")
            self._tokenizer = AutoTokenizer.from_pretrained(MODEL_HF_NAME, **tokenizer_kwargs)
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token

            # Modèle
            logger.info("Chargement du modèle...")
            if DEVICE == "cuda" and torch.cuda.is_available():
                model_kwargs["device_map"] = "auto"
                logger.info("Utilisation du GPU avec device_map=auto")
            else:
                logger.info("Utilisation du CPU")

            self._model = AutoModelForCausalLM.from_pretrained(MODEL_HF_NAME, **model_kwargs)

            # Pipeline
            device_index = 0 if DEVICE == "cuda" and torch.cuda.is_available() else -1
            self._pipeline = pipeline(
                "text-generation",
                model=self._model,
                tokenizer=self._tokenizer,
                device=device_index,
                return_full_text=False
            )

            logger.info("Modèle et pipeline chargés avec succès depuis Hugging Face Hub !")

        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle depuis Hub: {str(e)}")
            raise RuntimeError(f"Impossible de charger le modèle depuis Hugging Face Hub: {e}")

    def query_with_context(self, question: str, retrieved_chunks: List[str]) -> str:
        """Génère un guide pas à pas basé sur les documents fournis."""
        try:
            context_text = "\n\n".join(f"[Document {i}]\n{chunk}" for i, chunk in enumerate(retrieved_chunks, start=1))

            system_prompt = (
                "Tu es un assistant expert chargé de créer des guides pas à pas. "
                "Tu DOIS répondre EXCLUSIVEMENT en français. "
                "Fournis des réponses sous forme d'un guide clair, structuré en étapes numérotées. "
                "Ne montre jamais tes étapes de réflexion ou calcul, donne uniquement le guide final. "
                "Utilise uniquement les informations fournies ; si elles sont absentes, "
                "indique « Information non trouvée dans les documents fournis »."
            )

            prompt = f"""<|system|>
{system_prompt}

<|user|>
Contexte (documents fournis) :
{context_text}

Question : {question}

<|assistant|>
"""

            response = self._pipeline(
                prompt,
                max_new_tokens=800,
                temperature=0.7,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self._tokenizer.eos_token_id,
                eos_token_id=self._tokenizer.eos_token_id
            )

            generated_text = response[0]['generated_text'].strip()
            return self._clean_response(generated_text)

        except Exception as e:
            logger.error(f"Erreur lors de l'inférence LLM: {str(e)}")
            return f"Erreur lors de l'inférence : {e}"

    def generate_response(self, prompt: str, **kwargs) -> str:
        """Génère une réponse libre pour un prompt donné."""
        try:
            max_tokens = kwargs.get('max_tokens', 800)
            temperature = kwargs.get('temperature', 1.0)
            top_p = kwargs.get('top_p', 0.95)

            response = self._pipeline(
                prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self._tokenizer.eos_token_id,
                eos_token_id=self._tokenizer.eos_token_id
            )

            generated_text = response[0]['generated_text'].strip()
            return self._clean_response(generated_text)

        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse: {str(e)}")
            return f"Erreur lors de la génération : {e}"

    def _clean_response(self, text: str) -> str:
        """Nettoie la réponse générée."""
        import re
        text = text.replace("<|system|>", "")
        text = text.replace("<|user|>", "")
        text = text.replace("<|assistant|>", "")
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def get_model_info(self) -> Dict:
        """Retourne des informations sur le modèle chargé."""
        return {
            "model_name": MODEL_HF_NAME,
            "device": DEVICE,
            "model_loaded": self._model is not None,
            "tokenizer_loaded": self._tokenizer is not None
        }