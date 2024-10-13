import uuid

from sqlmodel import Field, SQLModel

class AnalizeText(SQLModel):
    text: str = Field(nullable=False)
    folders_ids: list[uuid.UUID]

class AnalizeListText(SQLModel):
    simples: list[AnalizeText]

class ShortlyModel(SQLModel):
    folders_ids: list[uuid.UUID]