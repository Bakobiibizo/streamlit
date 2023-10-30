import loguru
from typing import Dict

logger = loguru.logger


def create_message(message: str, role: str) -> Dict[str, str]:
    logger.info("Creating Message")
    message_dict = {
        "assistant": {"role": "assistant", "content": message},
        "user": {"role": "user", "content": message},
        "system": {"role": "system", "content": message},
    }
    return message_dict[role]
