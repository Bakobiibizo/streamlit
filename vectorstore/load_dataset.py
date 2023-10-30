import dataset
import pandas as pd
import loguru
import json
import re
import os
from pathlib import Path
from dotenv import load_dotenv
from datasets import load_dataset
from vectorstore.pinecone_client import PineconeClient
from vectorstore.embed_function import EmbeddingFunction

load_dotenv()

logger = loguru.logger

path = Path

BATCH_SIZE = 100

embed = EmbeddingFunction()
pinecone = PineconeClient()

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT")
host = os.getenv("PINECONE_INDEX_NAME")
index = os.getenv("PINECONE_PROJECT_NAME")
corpus_path = path.cwd() / "corpus" / "corpus.json"


def save_dataset_to_corpus(name="nampdn-ai/tiny-textbooks"):
    # If the dataset is gated/private, make sure you have run huggingface-cli login
    dataset = load_dataset(name)

    df = pd.DataFrame(dataset["train"])

    json_object = df.to_json(orient="records")

    # logger.debug(json_object[:1000])
    corpus_path.write_text(json_object, encoding="utf-8")


def extract_glossary_and_title(data_point):
    textbook_content = data_point.get("textbook", "")

    data_id = (data_point["s"] + data_point["idx"],)
    # Log metadata
    metadata = {
        "title": data_point["source"],
    }
    # logger.debug(f"\nmetadata - {metadata}\n")

    return data_id, metadata


@logger.catch
def main():
    data = json.loads(corpus_path.read_text(encoding="utf-8"))
    logger.debug(f"\ndata - {data[:1]}\n")

    vectors_to_upsert = []

    for item in data:
        text = item["text"]
        data_id, metadata = extract_glossary_and_title(item)

        sentences = embed.chunk_sentences(text=text)

        for idx, sentence in enumerate(sentences):
            embedding = embed.embed_sentence(sentence)

            vector_id = f"{data_id}-sentence-{idx}"
            vectors_to_upsert = vector_id, embedding, metadata

            # If we reach the batch size, upsert and clear the list
            if len(vectors_to_upsert) >= BATCH_SIZE:
                pinecone.upsert_vectors(vectors_to_upsert)
                vectors_to_upsert.clear()


if __name__ == "__main__":
    main()
