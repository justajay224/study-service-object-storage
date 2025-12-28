from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from src.controller.backblaze_controller import BackblazeController

router = APIRouter()
controller = BackblazeController()
path_group = "file"

@router.post("/{path_group}/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    return await controller.upload_file(file, background_tasks)

@router.get("/{path_group}/status/{temp_id}")
async def check_upload_status(temp_id: str):
    return await controller.check_upload_status(temp_id)

@router.get("/{path_group}/all-files")
async def get_all_files():
    return await controller.get_all_files()

@router.get("/{path_group}/{file_id}")
async def get_file_byID(file_id: str):
    return await controller.get_file_byID(file_id)

@router.put("/{path_group}/update/{file_id}")
async def update_file(file_id: str, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    return await controller.update_file(file_id, file, background_tasks)

@router.delete("/{path_group}/delete/{file_id}")
async def delete_file(file_id: str):
    return await controller.delete_file(file_id)