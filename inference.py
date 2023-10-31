import json
import os
from typing import List, Optional

import loguru
import requests
from langchain.llms import llamacpp

from templates import PROMPT_TEMPLATE

logger = loguru.logger

logger.info("Inference - Starting")


class Mistral(llamacpp.LlamaCpp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("Starting Mistral")
        self.url = "http://18.118.180.78:9091"
        self.headers = {
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip,deflate",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        }
        self.prompt_template = PROMPT_TEMPLATE
        self.prompt = self.get_prompt()

    def create_message(message: str, role: str) -> dict[str, str]:
        logger.info("Creating Message")
        message_dict = {
            "assistant": {"role": "assistant", "content": message},
            "user": {"role": "user", "content": message},
            "system": {"role": "system", "content": message},
        }
        return message_dict[role]

    def get_prompt(
        self,
        stream: Optional[bool] = True,
        n_predict: Optional[int] = 400,
        temperature: Optional[float] = 0.7,
        stop: Optional[List[str]] = ["</s>", "Llama:", "User:"],
        repeat_last_n: Optional[int] = 256,
        repeat_penalty: Optional[float] = 1.18,
        top_k: Optional[int] = 40,
        top_p: Optional[float] = 0.5,
        tfs_z: Optional[int] = 1,
        typical_p: Optional[int] = 1,
        presence_penalty: Optional[float] = 0,
        frequency_penalty: Optional[float] = 0,
        mirostat: Optional[float] = 0,
        mirostat_tau: Optional[float] = 5,
        mirostat_eta: Optional[float] = 0.1,
        grammar: Optional[str] = "",
        n_probs: Optional[int] = 0,
    ):
        logger.info("getting prompt")
        return {
            "stream": stream,
            "n_predict": n_predict,
            "temperature": temperature,
            "stop": stop,
            "repeat_last_n": repeat_last_n,
            "repeat_penalty": repeat_penalty,
            "top_k": top_k,
            "top_p": top_p,
            "tfs_z": tfs_z,
            "typical_p": typical_p,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "mirostat": mirostat,
            "mirostat_tau": mirostat_tau,
            "mirostat_eta": mirostat_eta,
            "grammar": grammar,
            "n_probs": n_probs,
            "prompt": self.prompt,
        }

    def inference(self, user_messages: list[dict[str, str]], query_text: str) -> str:
        messages = []
        system_message = json.dumps(
            self.create_messages(message=self.prompt, role="system")
        )
        messages.append(system_message)
        messages.append(json.dumps(message for message in user_messages))
        json.dumps(messages)

        logger.info(user_messages)
        response = requests.post(
            url=self.url,
            json=json.dumps(self.get_prompt),
            headers=self.headers,
            timeout=600,
        )
        logger.info(response)
        return response
