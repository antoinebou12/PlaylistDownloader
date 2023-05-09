from fastapi import APIRouter
from services import youtube

router = APIRouter()

@router.get('/{inputname}')
async def youtube_downloader(inputname: str):
    return await youtube.download(inputname)

