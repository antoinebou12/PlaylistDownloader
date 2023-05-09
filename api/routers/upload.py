from fastapi import APIRouter, UploadFile, File, HTTPException
from services import upload

router = APIRouter()

@router.post('/')
async def upload_file(file: UploadFile = File(...)):
    result = await upload.save_file(file)
    if result:
        return {"message": "Upload successful"}
    raise HTTPException(status_code=400, detail="Invalid filename or extension")
