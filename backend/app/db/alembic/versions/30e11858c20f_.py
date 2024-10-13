"""empty message

Revision ID: 30e11858c20f
Revises: 
Create Date: 2024-10-11 20:24:31.968405

"""
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa
import sqlmodel
from app.config import getSettings
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '30e11858c20f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создание таблицы usertable
    op.create_table(
        "usertable",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("password", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("api_key", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("usertable", sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_index(op.f("ix_usertable_email"), "usertable", ["email"], unique=True)

    # Создание нового пользователя
    new_user = {
        "id": str(uuid.uuid4()),
        "username": "superadmin",
        "password": getSettings().PWD_CONTEXT.hash("superadmin"),
        "email": "superadmin@example.com",
        "type": "superadmin",
    }

    # Создание объекта MetaData
    metadata = sa.MetaData()
    # Загружаем таблицу usertable
    usertable = sa.Table("usertable", metadata, autoload_with=op.get_bind())
    # Вставка нового пользователя в таблицу
    op.bulk_insert(usertable, [new_user])

    # Создание таблицы folders
    op.create_table(
        "folderstable",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Создание таблицы files
    op.create_table(
        "filestable",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("folder_id", sa.Uuid(), sa.ForeignKey("folderstable.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=datetime.now),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    # Удаление таблицы files
    op.drop_table("filestable")
    # Удаление таблицы folders
    op.drop_table("folderstable")
    # Удаление индекса и таблицы usertable
    op.drop_index(op.f("ix_usertable_email"), table_name="usertable")
    op.drop_table("usertable")
