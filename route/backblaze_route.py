from fastapi import APIRouter
from src.controller.backblaze_controller import BackblazeController, UploadRequest, UpdateRequest

router = APIRouter()
controller = BackblazeController()

@router.post("/images/upload")
async def upload_file(request: UploadRequest):
    return await controller.upload_file(request)

@router.get("/images/all-files")
async def get_all_files():
    return await controller.get_all_files()

@router.get("/images/{file_id}")
async def get_file_byID(file_id: str):
    return await controller.get_file_byID(file_id)

@router.patch("/images/{file_id}")
async def update_file(file_id: str, request: UpdateRequest):
    return await controller.update_file(file_id, request)

@router.delete("/images/{file_id}")
async def delete_file(file_id: str):
    return await controller.delete_file(file_id)