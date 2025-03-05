# from fastapi import APIRouter, UploadFile, File
# from src.service.backblaze_service import BackblazeService

# router = APIRouter()

# @router.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     # Baca file dan upload ke Backblaze B2
#     file_data = await file.read()
    
#     backblaze_service = BackblazeService()
#     file_id = backblaze_service.upload_file(file.filename, file_data)
    
#     return {"message": "File uploaded successfully", "file_id": file_id}
