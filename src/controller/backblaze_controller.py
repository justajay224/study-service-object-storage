from pydantic import BaseModel
import os
from fastapi import Response
from src.service.backblaze_service import BackblazeService
from utils.response_api import generate_success, generate_error 
from cryptography.fernet import InvalidToken
from utils.encryption_id import encrypt_data, decrypt_data

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
        try:
            file_id = self.service.upload_file(request.filename, request.file_data)
            
            encrypted_id = encrypt_data(file_id)
            
            base_url = os.getenv("BASE_URL").rstrip('/')
            url = f"{base_url}/media/{encrypted_id}" 
            
            return generate_success(
                data={"url": url}, 
                message="File uploaded", 
                code=201
            )
        except Exception as e:
            return generate_error(str(e), 500, "0004")

    async def get_file_byID(self, file_id: str):
        try:
            decrypted_id = decrypt_data(file_id)
        except InvalidToken:
            return generate_error("Invalid file ID", 400, "0006")
        except Exception as e:
            return generate_error(f"Decryption error: {str(e)}", 500, "0007")
        
        try:
            file_data, filename = self.service.get_file_byID(decrypted_id)
            
            content_type = "application/octet-stream"
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                content_type = "image/jpeg"
            elif filename.lower().endswith(('.mp4', '.mov', '.mkv')):
                content_type = "video/mp4"
            
            return Response(
                content=file_data,
                media_type=content_type,
                headers={
                    "Content-Disposition": f"inline; filename={filename}",
                    "Cache-Control": "no-cache, no-store, must-revalidate"
                }
            )
        except Exception as e:
            return generate_error(str(e), 500, "0005")

    
    async def get_all_files(self):
        try:
            files = self.service.get_all_files()
            
            files_with_encrypted = []
            for file in files:
                encrypted_id = encrypt_data(file['fileId'])  
                files_with_encrypted.append({
                    **file,
                    "encryptId": encrypted_id,
                    "fileId": file['fileId']  
                })
                
            return generate_success(
                data={"files": files_with_encrypted},
                message="OK",
                code=200
            )
        except KeyError as e:
            return generate_error(f"Invalid file format: {str(e)}", 500, "0006")
        except Exception as e:
            return generate_error(str(e), 500, "0006")
        
    async def update_file(self, file_id: str, request: UpdateRequest):
        try:
            decrypted_id = decrypt_data(file_id)
        except InvalidToken:
            return generate_error("Invalid file ID", 400, "0006")
        except Exception as e:
            return generate_error(f"Decryption error: {str(e)}", 500, "0007")
        
        try:
            new_file_id = self.service.update_file(decrypted_id, request.filename, request.file_data)
            
            encrypted_id = encrypt_data(new_file_id)
            
            base_url = os.getenv("BASE_URL").rstrip('/')
            url = f"{base_url}/media/{encrypted_id}" 
            return generate_success(
                data={"url" : url},
                message="File updated",
                code=200
            )
        except Exception as e:
            return generate_error(str(e), 500, "0009")
        
    async def delete_file(self, file_id: str):
        try:
            decrypted_id = decrypt_data(file_id)
        except InvalidToken:
            return generate_error("Invalid file ID", 400, "0006")
        except Exception as e:
            return generate_error(f"Decryption error: {str(e)}", 500, "0007")
        
        try:
            self.service.delete_file(decrypted_id)
            return generate_success(
                data=None,
                message="File deleted successfully",
                code=200
            )
        except Exception as e:
            if "not found" in str(e).lower():
                return generate_error("File not found", 404, "0010")
            return generate_error(str(e), 500, "0010")
