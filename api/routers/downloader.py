from fastapi import APIRouter
from services import downloader

router = APIRouter()

@router.get('/{inputname}')
async def downloader(inputname: str):
    return await downloader.download(inputname)
