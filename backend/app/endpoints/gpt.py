from fastapi import APIRouter, Depends, HTTPException, Request
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import getSession
from app.models import FoldersTable, FilesTable
from app.repositories.files import getFolder, getFilesByFolder, getFile
from app.utils.pdf import pdfToText
from app.utils.haikuGpt import assayText
from app.models import AssayTextModel
from starlette import status

apiRouter = APIRouter(prefix="/gpt", tags=["GPT"])


@apiRouter.post(
    "/analyze",
    status_code=status.HTTP_200_OK,
)
async def gpt(analyze_data: AssayTextModel, session: AsyncSession = Depends(getSession)):
    requirment_texts = []
    for folder_id in analyze_data.list:
        folder = await getFolder(session, folder_id)
        if not folder:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
        
        files_ids = await getFilesByFolder(session, folder_id)
        if not files_ids:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not have files")

        for file in files_ids:
            file_url = f"./files/{folder.name}/{file.name}"
            pdfText = await pdfToText(file_url)
            requirment_texts.append(pdfText)

    final_text = await assayText(analyze_data.text, requirment_texts)
    
    return final_text