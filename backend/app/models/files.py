import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

class FoldersTable(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=False)


class FilesTable(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=False)
    folder_id: uuid.UUID = Field(foreign_key="folderstable.id")
    created_at: datetime = Field(nullable=False, default=datetime.now())

class AssayTextModel(SQLModel):
    text: str = Field(nullable=False)
    list: list[uuid.UUID]