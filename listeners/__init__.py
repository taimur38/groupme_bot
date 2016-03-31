from . import task
from . import logger
from . import links
from . import emotion

listeners = [
    task.onMessage,
    logger.onMessage,
    links.onMessage,
    emotion.onMessage
]
