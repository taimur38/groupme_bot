from . import task
from . import logger
from . import links
from . import emotion
from . import description

listeners = [
    task.onMessage,
    logger.onMessage,
    links.onMessage,
    emotion.onMessage,
    description.onMessage
]
