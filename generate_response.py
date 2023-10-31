import os

import loguru
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import pinecone

from embedding_function import EmbeddingFunction
from inference import Mistral

logger = loguru.logger


def generate_document_response(uploaded_file, query_text):
    logger.info("Generating Response")

    logger.info("loading document")
    if uploaded_file is not None:
        documents = [uploaded_file.read().decode()]
    else:
        logger.exception("No file uploaded")
        raise ValueError("No file uploaded")

    logger.info("splitting document")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.create_documents(documents)

    logger.info("embedding documents")
    embedding_function = EmbeddingFunction()
    for text in texts:
        sentences = embedding_function.chunk_sentences(text.page_content)
        embeddings = embedding_function.embed_sentence(sentences)

    logger.info("creating pinecone client")
    db = pinecone.Pinecone(
        embedding=embeddings,
        index=os.getenv("PINECONE_INDEX"),
        text_key="text",
        distance_strategy="cosine",
    )

    logger.info("creating retriever")
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    logger.info("creating qa")
    qa = RetrievalQA.from_chain_type(
        llm=Mistral, chain_type="stuff", retriever=retriever
    )

    logger.info("running qa")
    return qa.run(query_text)
