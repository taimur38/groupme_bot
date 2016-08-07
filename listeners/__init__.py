from . import task
from . import randrand
from . import logger
from . import links
from . import emotion
from . import description
from . import reddit

listeners = [
    task.onMessage,
    logger.onMessage,
    links.onMessage,
    emotion.onMessage,
    description.onMessage,
    reddit.onMessage,
    randrand.onMessage
]
