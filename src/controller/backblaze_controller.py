from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
from typing import Optional
from src.service.backblaze_service import BackblazeService
from src.validation.file_validation import validate_file_extension, validate_file_size

class UploadRequest(BaseModel):
    filename: str
    file_data: str 

class BackblazeController:
    def __init__(self):
        self.service = BackblazeService()

    async def upload_file(self, request: UploadRequest):
        # Validasi ekstensi file
        if not validate_file_extension(request.filename):
            return self._generate_error("Invalid file extension", 400, "0001")

        # Validasi ukuran file 
        try:
            decoded_data = base64.b64decode(request.file_data)
        except Exception as e:
            return self._generate_error("Invalid base64", 400, "0003")

        if not validate_file_size(len(decoded_data)):
            return self._generate_error("File too large", 400, "0002")


        try:
            file_id = self.service.upload_file(request.filename, request.file_data)
            return self._generate_success(
                data={"fileId": file_id}, 
                message="File uploaded", 
                code=201
            )
        except Exception as e:
            return self._generate_error(str(e), 500, "0004")

    async def download_file(self, file_id: str):
        try:
            base64_data = self.service.download_file(file_id)
            return self._generate_success(
                data={"file_data": base64_data},
                message="OK",
                code=200
            )
        except Exception as e:
            return self._generate_error(str(e), 500, "0005")

    async def list_files(self):
        try:
            files = self.service.list_files()
            return self._generate_success(
                data={"files": files},
                message="OK",
                code=200
            )
        except Exception as e:
            return self._generate_error(str(e), 500, "0006")

    def _generate_success(self, data: dict, message: str, code: int):
        return JSONResponse(
            content={
                "metaData": {
                    "message": message,
                    "code": code,
                    "response_code": "0000"  
                },
                "data": data
            },
            status_code=code
        )

    def _generate_error(self, message: str, code: int, response_code: str):
        return JSONResponse(
            content={
                "metaData": {
                    "message": message,
                    "code": code,
                    "response_code": response_code
                },
                "data": None
            },
            status_code=code
        )