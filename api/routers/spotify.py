from fastapi import APIRouter
from services import spotify

router = APIRouter()

@router.get('/{inputname}')
async def spotify_downloader(inputname: str):
    return await spotify.download(inputname)
