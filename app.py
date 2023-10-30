import loguru
import streamlit as st
import json
from vectorstore.pinecone_client import PineconeClient
from vectorstore.embed_function import EmbeddingFunction
from inference.inference import inference
from chat.messages import create_message
from chat.templates import PROMPT_TEMPLATE

logger = loguru.logger

logger.info("App - Starting")

embeddings = EmbeddingFunction(
    model="multi-qa-MiniLM-L6-cos-v1",
    dimensions=768,
)
client = PineconeClient()


def main():
    st.title("📄 Knowledge Base")
    menu = ["Query", "Upload"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Query":
        st.subheader("❓ Query")
        session_memory = st.session_state
        if "messages" not in session_memory:
            session_memory.messages = []

        for message in session_memory.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Submit Report"):
            update_messages(session_memory, prompt)

    elif choice == "Upload":
        st.subheader("⬆️ Upload Files")
        if document := st.file_uploader("Upload File", type=["txt"]):
            if st.button("Upload"):
                meta_data = document.name
                document_id = document.file_id
                document_content = document.read()

                # Debug: Log the type and content of the document
                logger.debug(
                    f"Document content type: {type(document_content)}, content: {document_content}"
                )

                # Assuming document.read() returns bytes, decode it
                document_content_str = document_content.decode("utf-8")

                # Debug: Log the decoded content
                logger.debug(f"Decoded document content: {document_content_str}")

                embedding = embeddings.embed_sentence(document_content_str)

                logger.debug(f"Embedding type: {type(embedding)}, value: {embedding}")

                client.upsert_vectors(document_id, embedding, meta_data)


def update_messages(session_memory, prompt):
    message = create_message(prompt, "user")
    template = create_message(PROMPT_TEMPLATE, "system")
    session_memory.messages.append(message)
    prompt = [template, message]

    with st.chat_message("user"):
        st.markdown(message)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = inference(prompt)

        for chunk in assistant_response:
            full_response += f"{chunk} "
            message_placeholder.markdown(f"{full_response}▌")
        message_placeholder.markdown(full_response)
    message = create_message(full_response, "assistant")
    session_memory.messages.append(message)
    logger.debug(session_memory.messages)


if __name__ == "__main__":
    main()
