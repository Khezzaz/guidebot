from abc import ABC, abstractmethod
from typing import List, Dict

class LlmInterface(ABC):
    @abstractmethod
    def query_with_context(self, question: str, retrieved_chunks: List[str]) -> str:
        """Interroge le LLM avec un contexte fourni"""
        pass
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Génère une réponse à partir d'un prompt"""
        pass