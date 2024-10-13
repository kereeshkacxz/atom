from .healhCheck import apiRouter as healhCheck
from .user import apiRouter as User
from .files import apiRouter as Files
from .gpt import apiRouter as GPT


listOfRoutes = [
    healhCheck,
    User,
    Files,
    GPT,
]

__all__ = [
    "listOfRoutes",
]
