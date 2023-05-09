from fastapi import APIRouter
from services import soundcloud

router = APIRouter()


@router.get("/{inputname}")
async def soundcloud_downloader(inputname: str):
    return await soundcloud.download(inputname)
