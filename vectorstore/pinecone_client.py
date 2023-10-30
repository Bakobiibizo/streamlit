import loguru
import os
import pinecone
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

logger = loguru.logger

logger.info("VectorDB - Starting")


class PineconeClient:
    def __init__(
        self,
        model: Optional[str] = "multi-qa-MiniLM-L6-cos-v1",
    ):
        self.model = model
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.index = pinecone.Index(self.index_name)
        self.pinecone = pinecone
        self.pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            host=os.getenv("PINECONE_URL"),
            environment=os.getenv("PINECONE_ENVIRONMENT"),
        )

    def create_index(self, dimensions: Optional[int] = 768):
        self.pinecone.create_index(self.index_name, dimensions=dimensions)

    def list_indexes(self):
        return self.pinecone.list_indexes()

    def describe_index(self):
        return self.pinecone.describe_index(self.index_name)

    def delete_index(self):
        return self.pinecone.delete_index(self.index_name)

    def scale_replicas(self, new_number_of_replicas: int = 4):
        return self.pinecone.configure_index(
            self.index_name, replicas=new_number_of_replicas
        )

    def describe_index_statstics(self):
        return self.index.describe_index_stats()

    def upsert_vectors(self, vectors):
        results = []
        for vector in vectors:
            logger.debug(
                f"Vector for Pinecone upsert type: {type(vectors)}, value: {vectors}"
            )

            vector_id, vectors, vector_metadata = vectors

            vector_data = (vector_id, vectors, vector_metadata)
            results.append(self.index.upsert(vector_data))
        return results

    def query_index(
        self,
        vector: List[int],
        vector_filter: Dict[str, Dict[str, List[str]]],
        top_k: int,
        include_values: bool = True,
        include_metadata: bool = True,
    ):
        return self.index.query(
            namespace=self.index,
            top_k=top_k,
            vector=vector,
            filter=vector_filter,
            include_values=include_values,
            include_metadata=include_metadata,
        )

    def delete_vectors(self, ids: List[str]):
        return self.index.delete(ids=[ids], namespace=self.index_name)

    def fetch_vectors(self, ids: List[str]):
        return self.index.fetch(ids=ids, namespace=self.index_name)

    def update_vectors(
        self, vector_id: str, vector: List[float], metadata: Dict[str, str]
    ):
        return self.index.update(id=vector_id, vector=vector, metadata=metadata)

    def create_collection(self, collection_name: str):
        self.pinecone.create_collection(name=collection_name, source=self.index_name)

    def list_collections(self):
        return self.pinecone.list_collections()

    def describe_collection(self, collection_name: str):
        return self.pinecone.describe_collection(collection_name)

    def delete_collection(self, collection_name: str):
        return self.pinecone.delete_collection(collection_name)


if __name__ == "__main__":
    pinecone_client = PineconeClient()
    print(pinecone_client.create_index(1536))
