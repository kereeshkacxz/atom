from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated

import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import getSession
from app.models import FoldersTable, FilesTable
from app.repositories.files import getFolder, getFilesByFolder, getFile
from app.utils.auth import getCurrentUser
from app.utils.pdf import pdfToText
from app.utils.haikuGpt import assayText, textFormat
from app.models import AnalizeText, AnalizeListText, UserTable, ShortlyModel
from app.static.pattern import pattern
from app.static.dictOfDecriptions import descriptions_dict

from starlette import status

apiRouter = APIRouter(prefix="/gpt", tags=["GPT"])


@apiRouter.post(
    "/analyze",
    status_code=status.HTTP_200_OK,
)
async def gpt(analyze_data: AnalizeText, current_user: Annotated[UserTable, Depends(getCurrentUser)], session: AsyncSession = Depends(getSession)):
    requirment_texts = []
    for folder_id in analyze_data.folders_ids:
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

    final_text = await assayText(analyze_data.text, requirment_texts, current_user.api_key)
    
    return final_text

@apiRouter.post(
    "/analyze_list",
    status_code=status.HTTP_200_OK,
)
async def gpt(analyze_data: AnalizeListText, current_user: Annotated[UserTable, Depends(getCurrentUser)], session: AsyncSession = Depends(getSession)):
    summ_answer = {}
    summ_answer['list_answers'] = []
    statistics = {'positive': 0, 'negative': 0}
    for analyze_simple in analyze_data.simples:
        requirment_texts = []
        for folder_id in analyze_simple.folders_ids:
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

        final_text = await assayText(analyze_simple.text, requirment_texts, current_user.api_key)

        if final_text['result'] == 'Match':
            statistics['positive'] += 1
        else:
            statistics['negative'] += 1
        
        summ_answer['list_answers'].append(final_text)
    summ_answer['statistics'] = statistics
        
    return summ_answer

@apiRouter.post(
    "/normalize",
    status_code=status.HTTP_200_OK,
)
async def text_format(text: str, current_user: Annotated[UserTable, Depends(getCurrentUser)]):
    format_text = await textFormat(text, pattern, current_user.api_key)
    return {'normalize_text': format_text}

@apiRouter.post(
    "/shortly",
    status_code=status.HTTP_200_OK,
)
async def text_shortly(data: ShortlyModel, session: AsyncSession = Depends(getSession)):
    summ_dict = {}
    for folder_id in data.folders_ids:
        folder = await getFolder(session, folder_id)
        if not folder:
            continue

        if folder.name in descriptions_dict:
            text = descriptions_dict[folder.name]
        else:
            text = 'Uups'
          
        summ_dict[folder.id] = [folder.name, text]
    return summ_dict
