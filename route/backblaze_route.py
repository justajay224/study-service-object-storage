from fastapi import APIRouter
from src.controller.backblaze_controller import BackblazeController, UploadRequest, UpdateRequest
from src.validation.file_validation import validate_upload_request, validate_update_request

controller = BackblazeController()

pathgroup = "media"
router = APIRouter(prefix=f"/{pathgroup}")

@router.post("/")
async def upload_file(request: UploadRequest):
    if error := validate_upload_request(request.filename, request.file_data):
        return error
    return await controller.upload_file(request)

@router.get("/all-files")
async def get_all_files():
    return await controller.get_all_files()

@router.get("/{file_id}")
async def get_file_byID(file_id: str):
    return await controller.get_file_byID(file_id)

@router.patch("/{file_id}")
async def update_file(file_id: str, request: UpdateRequest):
    if error := validate_update_request(request.filename, request.file_data):
        return error
    return await controller.update_file(file_id, request)

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    return await controller.delete_file(file_id)