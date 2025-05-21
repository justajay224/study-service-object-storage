from fastapi import APIRouter
from src.controller.backblaze_controller import BackblazeController, UploadRequest, UpdateRequest

controller = BackblazeController()

pathgroup = "images"
router = APIRouter(prefix=f"/{pathgroup}")

@router.post("/upload")
async def upload_file(request: UploadRequest):
    return await controller.upload_file(request)

@router.get("/all-files")
async def get_all_files():
    return await controller.get_all_files()

@router.get("/{file_id}")
async def get_file_byID(file_id: str):
    return await controller.get_file_byID(file_id)

@router.patch("/{file_id}")
async def update_file(file_id: str, request: UpdateRequest):
    return await controller.update_file(file_id, request)

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    return await controller.delete_file(file_id)
