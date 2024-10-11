import os
import uuid
from sqlmodel import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException

from app.models import FilesTable, FoldersTable

BASE_DIR = './files'  # Убедитесь, что путь корректен

async def getFolders(session: AsyncSession) -> list[FoldersTable]:
    statement = select(FoldersTable)
    folders = await session.execute(statement)
    return folders.scalars().all()

async def createFolder(session: AsyncSession, name: str) -> FoldersTable:
    folder = FoldersTable(name=name)
    session.add(folder)
    await session.commit()
    await session.refresh(folder)

    # Создаем папку на файловой системе
    folder_path = os.path.join(BASE_DIR, str(folder.name))
    os.makedirs(folder_path, exist_ok=True)

    return folder

async def getFolder(session: AsyncSession, folder_id: uuid.UUID) -> FoldersTable | None:
    statement = select(FoldersTable).where(FoldersTable.id == folder_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def deleteFolder(session: AsyncSession, folder_id: uuid.UUID) -> bool:
    folder = await getFolder(session, folder_id)
    if not folder:
        return False

    statement = delete(FoldersTable).where(FoldersTable.id == folder_id)
    await session.execute(statement)
    await session.commit()

    # Удаляем папку с файловой системы
    folder_path = os.path.join(BASE_DIR, folder.name)
    if os.path.exists(folder_path):
        os.rmdir(folder_path)
    return True

async def createFile(session: AsyncSession, file: UploadFile, folder: FoldersTable) -> FilesTable:
    # Извлекаем имя файла из метаданных
    name = file.filename

    # Создаем запись в базе данных
    file_record = FilesTable(name=name, folder_id=folder.id)
    session.add(file_record)
    await session.commit()
    await session.refresh(file_record)

    # Создаем файл на файловой системе
    folder_path = os.path.join(BASE_DIR, folder.name)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, name)
    try:
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    return file_record

async def getFile(session: AsyncSession, file_id: uuid.UUID) -> FilesTable | None:
    statement = select(FilesTable).where(FilesTable.id == file_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def deleteFile(session: AsyncSession, file_id: uuid.UUID) -> bool:
    file_record = await getFile(session, file_id)
    if not file_record:
        return False

    # Получаем объект папки по folder_id
    folder_record = await getFolder(session, file_record.folder_id)
    if not folder_record:
        return False 

    # Формируем путь к файлу
    folder_path = os.path.join(BASE_DIR, folder_record.name)
    file_path = os.path.join(folder_path, file_record.name)
    
    if os.path.exists(file_path):
        os.remove(file_path)

    # Удаляем запись из базы данных
    statement = delete(FilesTable).where(FilesTable.id == file_id)
    await session.execute(statement)
    await session.commit()

    return True
