import uuid
from datetime import date

from sqlmodel import Field, SQLModel


class UserTable(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True, index=True)
    type: str | None = Field(default="user", nullable=False)

class UserSchema(SQLModel):
    username: str
    email: str
    type: str

class AuthSchema(SQLModel):
    email: str
    password: str
