from . import task
from . import logger
from . import links

listeners = [
    task.onMessage,
    logger.onMessage,
    links.onMessage
]
