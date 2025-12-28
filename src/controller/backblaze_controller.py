from fastapi import HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import base64
import mimetypes
import os
import uuid
import threading
from io import BytesIO
from typing import Optional, Dict
from dotenv import load_dotenv
from src.service.backblaze_service import BackblazeService
from utils.response_api import generate_success, generate_error 
from src.validation.file_validation import validate_file_extension, validate_file_size

load_dotenv()

class UpdateRequest(BaseModel):
    filename: str 
    file_data: str 

# Storage untuk mapping temp_id -> real_file_id
upload_status: Dict[str, dict] = {}

class BackblazeController:
    def __init__(self):
        self.service = BackblazeService()
        # Use default if BASE_URL is empty or not set
        self.base_url = os.getenv("BASE_URL") or "http://127.0.0.1:8000"

    def _background_upload(self, temp_id: str, filename: str, file_bytes: bytes):
        """Background task untuk upload file + pre-cache"""
        try:
            file_id = self.service.upload_file(filename, file_bytes)
            
            # PRE-CACHE: Simpan file ke cache langsung setelah upload
            # Sehingga GET pertama kali juga cepat!
            self.service.pre_cache_file(file_id, file_bytes, filename)
            
            upload_status[temp_id] = {
                "status": "completed",
                "file_id": file_id,
                "link": f"{self.base_url}/file/{file_id}"
            }
            print(f"[Upload] {temp_id} completed -> {file_id} (pre-cached)")
        except Exception as e:
            upload_status[temp_id] = {
                "status": "failed",
                "error": str(e)
            }
            print(f"[Upload] {temp_id} failed: {e}")

    async def upload_file(self, file: UploadFile, background_tasks: BackgroundTasks):
        """Upload file dengan background processing"""
        if not validate_file_extension(file.filename):
            return generate_error("Invalid file extension", 400, "0001")
        
        try:
            file_bytes = await file.read()
        except Exception as e:
            return generate_error("Failed to read file", 400, "0003")

        if not validate_file_size(len(file_bytes)):
            return generate_error("File too large", 400, "0002")

        # Generate temporary ID
        temp_id = str(uuid.uuid4())
        
        # Set initial status
        upload_status[temp_id] = {"status": "uploading"}
        
        # Run upload in background thread (not blocking)
        thread = threading.Thread(
            target=self._background_upload,
            args=(temp_id, file.filename, file_bytes)
        )
        thread.start()
        
        # Return immediately with temp_id
        return generate_success(
            data={
                "tempId": temp_id,
                "status": "uploading",
                "checkStatusUrl": f"{self.base_url}/file/status/{temp_id}"
            }, 
            message="Upload started", 
            code=202  # 202 Accepted
        )

    async def check_upload_status(self, temp_id: str):
        """Check status of background upload"""
        if temp_id not in upload_status:
            return generate_error("Upload ID not found", 404, "0011")
        
        status = upload_status[temp_id]
        
        if status["status"] == "completed":
            return generate_success(
                data={
                    "status": "completed",
                    "fileId": status["file_id"],
                    "link": status["link"]
                },
                message="Upload completed",
                code=200
            )
        elif status["status"] == "failed":
            return generate_error(status.get("error", "Upload failed"), 500, "0012")
        else:
            return generate_success(
                data={"status": "uploading"},
                message="Upload in progress",
                code=200
            )

    async def get_file_byID(self, file_id: str):
        """Get file dan return langsung sebagai file (StreamingResponse)"""
        try:
            file_data, filename = self.service.get_file_byID(file_id)
            
            # Detect content type
            content_type, _ = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = "application/octet-stream"
            
            return StreamingResponse(
                BytesIO(file_data),
                media_type=content_type,
                headers={
                    "Content-Disposition": f"inline; filename=\"{filename}\""
                }
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
        
    def _background_update(self, temp_id: str, old_file_id: str, filename: str, file_bytes: bytes):
        """Background task untuk update file"""
        try:
            new_file_id = self.service.update_file(old_file_id, filename, file_bytes)
            
            # PRE-CACHE file baru
            self.service.pre_cache_file(new_file_id, file_bytes, filename)
            
            upload_status[temp_id] = {
                "status": "completed",
                "file_id": new_file_id,
                "link": f"{self.base_url}/file/{new_file_id}"
            }
            print(f"[Update] {temp_id} completed -> {new_file_id} (pre-cached)")
        except Exception as e:
            upload_status[temp_id] = {
                "status": "failed",
                "error": str(e)
            }
            print(f"[Update] {temp_id} failed: {e}")

    async def update_file(self, file_id: str, file: UploadFile, background_tasks: BackgroundTasks):
        """Update file dengan background processing"""
        if not validate_file_extension(file.filename):
            return generate_error("Invalid file extension", 400, "0007")
        
        try:
            file_bytes = await file.read()
        except Exception as e:
            return generate_error("Failed to read file", 400, "0008")

        if not validate_file_size(len(file_bytes)):
            return generate_error("File too large", 400, "0002")
        
        # Generate temporary ID
        temp_id = str(uuid.uuid4())
        
        # Set initial status
        upload_status[temp_id] = {"status": "updating"}
        
        # Run update in background thread
        thread = threading.Thread(
            target=self._background_update,
            args=(temp_id, file_id, file.filename, file_bytes)
        )
        thread.start()
        
        # Return immediately with temp_id
        return generate_success(
            data={
                "tempId": temp_id,
                "status": "updating",
                "checkStatusUrl": f"{self.base_url}/file/status/{temp_id}"
            }, 
            message="Update started", 
            code=202
        )
        
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
