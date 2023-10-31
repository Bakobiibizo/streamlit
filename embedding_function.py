import os
from typing import Dict, List, Optional

import loguru
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from vectorstore.pinecone_client import PineconeClient

logger = loguru.logger


class EmbeddingFunction:
    def __init__(
        self,
        model: Optional[str] = "multi-qa-MiniLM-L6-cos-v1",
        dimensions: Optional[int] = 768,
    ):
        nltk.download("punkt")
        logger.info("starting embedding function")
        self.pinecone_client = PineconeClient()
        self.dimensions = dimensions
        self.model_string = model
        self.model = SentenceTransformer(model)

    def chunk_sentences(self, text: str) -> List[str]:
        logger.info("chunking sentence")
        return sent_tokenize(text)

    def embed_sentence(
        self, sentence: str, meta_data: Optional[str] = os.getenv("PINECONE_INDEX")
    ) -> Dict[str, str]:
        logger.info("embedding sentence")
        if not meta_data:
            return self.model.encode(sentence)
        return self.model.encode([sentence, meta_data])
