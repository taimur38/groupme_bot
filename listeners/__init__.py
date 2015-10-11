from . import task
from . import logger

listeners = [
    task.onMessage,
    logger.onMessage
]
