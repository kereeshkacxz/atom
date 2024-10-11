import uuid

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse


from app.db.connection import getSession
from app.models import FoldersTable, FilesTable
from app.repositories.files import createFile, deleteFile, getFile, getFolders, getFolder, createFolder, deleteFolder, getFilesByFolder
from app.utils.auth import isUserAdmin

apiRouter = APIRouter(prefix="", tags=["Files"])

# Эндпоинты для работы с папками

@apiRouter.post(
    "/folders/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(isUserAdmin)],
)
async def create_folder_item(folder_name: str, session: AsyncSession = Depends(getSession)):
    return await createFolder(session, folder_name)

@apiRouter.delete(
    "/folders/{folder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(isUserAdmin)],
)
async def delete_folder_item(folder_id: uuid.UUID, session: AsyncSession = Depends(getSession)):
    success = await deleteFolder(session, folder_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    return {"detail": "Folder deleted successfully"}


@apiRouter.get(
    "/folders/",
    response_model=list[FoldersTable],
    status_code=status.HTTP_200_OK,
)
async def read_all_folders(session: AsyncSession = Depends(getSession)):
    return await getFolders(session)

# Эндпоинты для работы с файлами

@apiRouter.get(
    "/files/",
    response_model=list[FilesTable],
    status_code=status.HTTP_200_OK,
)
async def read_files_in_folder(folder_id: uuid.UUID, session: AsyncSession = Depends(getSession)):
    folder = await getFolder(session, folder_id)
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    return await getFilesByFolder(session, folder_id)

@apiRouter.post(
    "/files/",
    response_model=FilesTable,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(isUserAdmin)],
)
async def create_file_item(folder_id: uuid.UUID, file: UploadFile = File(...), session: AsyncSession = Depends(getSession)):
    folder = await getFolder(session, folder_id)
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    return await createFile(session, file, folder)

@apiRouter.delete(
    "/files/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(isUserAdmin)],
)
async def delete_file_item(file_id: uuid.UUID, session: AsyncSession = Depends(getSession)):
    success = await deleteFile(session, file_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return {"detail": "File deleted successfully"}

@apiRouter.get(
    "/files/{file_id}",
    response_model=FilesTable,
    status_code=status.HTTP_200_OK,
)
async def read_file_item(file_id: uuid.UUID, request: Request, session: AsyncSession = Depends(getSession)):
    file = await getFile(session, file_id)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    folder = await getFolder(session, file.folder_id)
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    
    file_url = f"files/{folder.name}/{file.name}"
    full_url = f"{request.base_url}{file_url}"  # Создаем полный URL

    return RedirectResponse(url=full_url, status_code=status.HTTP_302_FOUND)
