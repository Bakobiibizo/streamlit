import os
import json
import loguru
import requests
from dotenv import load_dotenv

load_dotenv()

logger = loguru.logger

logger.info("Inference - Starting")


URL = os.getenv("MODEL_URL")
HEADERS = {
    "Accept": "text/event-stream",
    "Accept-Encoding": "gzip,deflate",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
}


def inference(user_messages: list[dict[str, str]]) -> str:
    body = {
  "stream": True,
  "n_predict": 400,
  "temperature": 0.7,
  "stop": [
    "</s>",
    "Llama:",
    "User:"
  ],
  "repeat_last_n": 256,
  "repeat_penalty": 1.18,
  "top_k": 40,
  "top_p": 0.5,
  "tfs_z": 1,
  "typical_p": 1,
  "presence_penalty": 0,
  "frequency_penalty": 0,
  "mirostat": 0,
  "mirostat_tau": 5,
  "mirostat_eta": 0.1,
  "grammar": "",
  "n_probs": 0,
  "prompt": json.dumps(user_messages)
    }
    try:
        response = requests.post(url=URL, json=body, headers=HEADERS)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data:'):
                json_data = json.loads(decoded_line[len('data: '):])

            # Debugging lines
            logger.debug(f"Status code: {json_data}")
            logger.debug(f"Raw response: {response.content}")

            return json.response
         
    except requests.JSONDecodeError:
        logger.error("Failed to decode JSON response")
        return logger.error(f"Request failed: {e}")

if __name__ == "__main__":
    response = inference([{"role":"system", "content": "you're a friendly and helpful chat bot"}, {"role":"user", "content": "hi there how are you?", "role": "llama", "content": ""}])
