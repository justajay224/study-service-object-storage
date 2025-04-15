from fastapi import APIRouter
from src.controller.backblaze_controller import BackblazeController, UploadRequest

router = APIRouter()
controller = BackblazeController()

@router.post("/upload")
async def upload_file(request: UploadRequest):
    return await controller.upload_file(request)

@router.get("/files")
async def list_files():
    return await controller.list_files()

@router.get("/download/{file_id}")
async def download_file(file_id: str):
    return await controller.download_file(file_id)