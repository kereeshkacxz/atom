from .healhCheck import apiRouter as healhCheck
from .user import apiRouter as User
from .files import apiRouter as Files


listOfRoutes = [
    healhCheck,
    User,
    Files,
]

__all__ = [
    "listOfRoutes",
]
