from .healhCheck import apiRouter as healhCheck
from .user import apiRouter as User


listOfRoutes = [
    healhCheck,
    User,
]

__all__ = [
    "listOfRoutes",
]
