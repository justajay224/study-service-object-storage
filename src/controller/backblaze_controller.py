from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
from typing import Optional
from src.service.backblaze_service import BackblazeService
from utils.response_api import generate_success, generate_error 
from src.validation.file_validation import validate_file_extension, validate_file_size

class UploadRequest(BaseModel):
    filename: str
    file_data: str 
    
class UpdateRequest(BaseModel):
    filename: str 
    file_data: str 

class BackblazeController:
    def __init__(self):
        self.service = BackblazeService()

    async def upload_file(self, request: UploadRequest):
        if not validate_file_extension(request.filename):
            return generate_error("Invalid file extension", 400, "0001")
        try:
            decoded_data = base64.b64decode(request.file_data)
        except Exception as e:
            return generate_error("Invalid base64", 400, "0003")

        if not validate_file_size(len(decoded_data)):
            return generate_error("File too large", 400, "0002")


        try:
            file_id = self.service.upload_file(request.filename, request.file_data)
            return generate_success(
                data={"fileId": file_id}, 
                message="File uploaded", 
                code=201
            )
        except Exception as e:
            return generate_error(str(e), 500, "0004")

    async def get_file_byID(self, file_id: str):
        try:
            base64_data = self.service.get_file_byID(file_id)
            return generate_success(
                data={"file_data": base64_data},
                message="OK",
                code=200
            )
        except Exception as e:
            return generate_error(str(e), 500, "0005")

    async def get_all_files(self):
        try:
            files = self.service.get_all_files()
            return generate_success(
                data={"files": files},
                message="OK",
                code=200
            )
        except Exception as e:
            return generate_error(str(e), 500, "0006")
        
    async def update_file(self, file_id: str, request: UpdateRequest):
        if not validate_file_extension(request.filename):
            return generate_error("Invalid file extension", 400, "0007")
        try:
            decoded_data = base64.b64decode(request.file_data)
        except Exception as e:
            return generate_error("Invalid base64", 400, "0008")

        if not validate_file_size(len(decoded_data)):
            return generate_error("File too large", 400, "0002")
        try:
            new_file_id = self.service.update_file(file_id, request.filename, request.file_data)
            return generate_success(
                data={"new_file_id": new_file_id},
                message="File updated",
                code=200
            )
        except Exception as e:
            return generate_error(str(e), 500, "0009")
        
    async def delete_file(self, file_id: str):
        try:
            self.service.delete_file(file_id)
            return generate_success(
                data=None,
                message="File deleted successfully",
                code=200
            )
        except Exception as e:
            # Handle error spesifik untuk file tidak ditemukan
            if "not found" in str(e).lower():
                return generate_error("File not found", 404, "0010")
            return generate_error(str(e), 500, "0010")
