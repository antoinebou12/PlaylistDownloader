from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse
from routers import downloader
from routers import soundcloud
from routers import spotify
from routers import upload
from routers import youtube

app = FastAPI()

app.include_router(soundcloud.router, prefix="/api/soundcloud")
app.include_router(youtube.router, prefix="/api/youtube")
app.include_router(spotify.router, prefix="/api/spotify")
app.include_router(downloader.router, prefix="/api/downloader")
app.include_router(upload.router, prefix="/api/upload")


@app.get("/api/view/{item}")
async def view_file(item: str):
    file_path = Path(app.config["UPLOAD_FOLDER"]) / item
    if file_path.is_file():
        return FileResponse(str(file_path))
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/api/playlist/{item}")
async def playlist_downloaded(item: str):
    file_path = Path(app.config["DOWNLOAD_FOLDER"]) / item
    if file_path.is_file():
        return FileResponse(str(file_path))
    raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
