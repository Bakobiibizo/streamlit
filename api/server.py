import requests
from uvicorn import run
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

URL = "http://hub.agentartificial.com:9091/"

HEADERS = {
    "Accept": "text/event-stream",
    "Accept-Encoding": "gzip,deflate",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
}


class UserRequest(BaseModel):
    prompt: str


class Message(BaseModel):
    role: str
    content: str


class History(BaseModel):
    history: List[Message]


TEMPLATE = Message(
    role="system",
    content="You are an expert transcription analysis and summarizer AI. You recieve user requests that consist of transcriptions of various types of conversations. You are very skilled at pulling salient points into key take aways. Also you extract key action items labeled with the speaker responsible for completion. After you complete that you provide a semantic analysis of the transcript. Finally you will create an executive summary of the document.",
)


class ContextHistory:
    def __init__(self):
        self.template: Message = TEMPLATE
        self.history: List[Message] = []

    def set_context(self, template: Optional[Message] = TEMPLATE) -> None:
        if not template:
            raise ValueError("No Template to set context")
        self.history.append(template)

    def add_to_history(self, message: Message) -> None:
        if not message:
            raise ValueError("No message to add to history")
        self.history.append(message)

    def get_history(self) -> str:
        content_history: str = ""
        if not self.history:
            return "You are a friendly and helpful chat bot"
        for message in self.history:
            if message.role == "system":
                content_history.join(f"{message.content}\\n\\n")
            elif message.role == "user":
                content_history.join(f"User: {message.content}\\n\\n")
            elif message.role == "assistant":
                content_history.join(f"Llama: {message.content}\\n\\n")
        return content_history

    def construct_prompt(self, message: Message) -> UserRequest:
        if not message:
            raise ValueError("No message to add to history")
        self.add_to_history(message)
        return self.get_history()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/chat")
def chat(user_request: UserRequest):
    return requests.post(
        url=URL,
        json=user_request.model_dump(),
        headers=HEADERS,
        timeout=60,
    ).json()


def main():
    run("server:app", host="0.0.0.0", port=8081, reload=True)


if __name__ == "__main__":
    main()
