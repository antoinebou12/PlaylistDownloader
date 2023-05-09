from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from services import upload

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    result = await upload.save_file(file)
    if result:
        return {"message": "Upload successful"}
    raise HTTPException(status_code=400, detail="Invalid filename or extension")
