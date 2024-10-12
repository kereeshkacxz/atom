from fastapi import APIRouter, Depends, HTTPException, Request
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import getSession
from app.models import FoldersTable, FilesTable
from app.repositories.files import getFolder, getFile
from app.utils.pdf import pdfToText
from app.utils.gpt import assayText
from app.models import AssayTextModel
from starlette import status

apiRouter = APIRouter(tags=["GPT"])


@apiRouter.post(
    "/gpt",
    status_code=status.HTTP_200_OK,
)
async def gpt(assay_text: AssayTextModel, session: AsyncSession = Depends(getSession)):
    file = await getFile(session, assay_text.file_id)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    folder = await getFolder(session, file.folder_id)
    if not folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    
    file_url = f"./files/{folder.name}/{file.name}"
    pdfText = await pdfToText(file_url)

    if not pdfText:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    final_text = await assayText(assay_text.text, pdfText)
    
    return final_text