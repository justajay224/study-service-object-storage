from src.repository.backblaze_repository import BackblazeRepository
import base64
import time
from functools import lru_cache
from collections import OrderedDict
from utils.encrypt_decrypt import encrypt_file, decrypt_file
from dotenv import load_dotenv
import os

# In-memory cache untuk file yang sudah di-decrypt
# Format: {file_id: {"data": bytes, "filename": str, "timestamp": float}}
class FileCache:
    def __init__(self, max_size=100, max_file_size=10*1024*1024):  # 100 files, max 10MB each
        self.cache = OrderedDict()
        self.max_size = max_size
        self.max_file_size = max_file_size
    
    def get(self, file_id: str):
        if file_id in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(file_id)
            print(f"[Cache] HIT: {file_id[:20]}...")
            return self.cache[file_id]
        print(f"[Cache] MISS: {file_id[:20]}...")
        return None
    
    def set(self, file_id: str, data: bytes, filename: str):
        # Skip caching if file too large
        if len(data) > self.max_file_size:
            print(f"[Cache] SKIP (too large): {len(data)} bytes")
            return
        
        # Remove oldest if cache full
        if len(self.cache) >= self.max_size:
            oldest = next(iter(self.cache))
            del self.cache[oldest]
            print(f"[Cache] EVICTED: {oldest[:20]}...")
        
        self.cache[file_id] = {
            "data": data,
            "filename": filename,
            "timestamp": time.time()
        }
        print(f"[Cache] STORED: {file_id[:20]}... ({len(data)} bytes)")
    
    def delete(self, file_id: str):
        if file_id in self.cache:
            del self.cache[file_id]
            print(f"[Cache] DELETED: {file_id[:20]}...")

# Global cache instance
_file_cache = FileCache()

class BackblazeService:
    def __init__(self):
        self.repository = BackblazeRepository()
        load_dotenv()
        self.encryption_key = os.getenv("ENCRYPTION_KEY") 
        key_base64 = os.getenv("ENCRYPTION_KEY")
        self.encryption_key = base64.b64decode(key_base64)
        if len(self.encryption_key) != 32:
            raise ValueError("Encryption key harus 32 byte (AES-256)!")
        
    def upload_file(self, filename: str, file_bytes: bytes) -> str:
        """Upload file dengan enkripsi AES-256"""
        try:
            encrypted_data = encrypt_file(file_bytes, self.encryption_key)
        except ValueError as e:
            raise ValueError(f"Encryption failed: {str(e)}") from e
        
        return self.repository.upload_file(filename, encrypted_data)

    def pre_cache_file(self, file_id: str, file_bytes: bytes, filename: str):
        """Pre-cache file setelah upload agar GET pertama cepat"""
        _file_cache.set(file_id, file_bytes, filename)

    def get_all_files(self):
        return self.repository.get_all_files()

    def get_file_byID(self, file_id: str) -> tuple[bytes, str]:
        """Get file by ID dengan caching"""
        # Check cache first
        cached = _file_cache.get(file_id)
        if cached:
            return cached["data"], cached["filename"]
        
        # Cache miss - download and decrypt
        encrypted_data, filename = self.repository.get_file_byID(file_id)
        decrypted_data = decrypt_file(encrypted_data, self.encryption_key)
        
        # Store in cache
        _file_cache.set(file_id, decrypted_data, filename)
        
        return decrypted_data, filename
    
    def update_file(self, file_id: str, new_filename: str, file_bytes: bytes) -> str:
        """Update file dengan file baru"""
        # Invalidate cache for old file
        _file_cache.delete(file_id)
        
        try:
            encrypted_data = encrypt_file(file_bytes, self.encryption_key)
            return self.repository.update_file(file_id, new_filename, encrypted_data)
        except Exception as e:
            raise ValueError(f"Update failed: {str(e)}")
        
    def delete_file(self, file_id: str) -> None:
        # Invalidate cache
        _file_cache.delete(file_id)
        
        try:
            self.repository.delete_file(file_id)
        except Exception as e:
            raise ValueError(f"Delete error: {str(e)}")