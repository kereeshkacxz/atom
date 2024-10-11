from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel

from app.config import getSettings


class RegistrationForm(SQLModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=8)
    email: EmailStr = Field(min_length=5)

    @field_validator("password")
    def hashPassword(cls, password):
        password = getSettings().PWD_CONTEXT.hash(password)
        return password


class RegistrationAdmin(RegistrationForm):
    type: str = Field(default="admin")


class RegistrationSuccess(SQLModel):
    message: str
