import fitz  # PyMuPDF
import asyncio

async def pdfToText(pdf_path):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _convert_pdf_to_txt, pdf_path)

def _convert_pdf_to_txt(pdf_path):
    # Открываем PDF файл
    document = fitz.open(pdf_path)
    text = ""
    # Проходим по каждой странице
    for page_num in range(len(document)):
        page = document.load_page(page_num) 
        text += page.get_text() 
    document.close()
    return text