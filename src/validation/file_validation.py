# Allowed file extensions
ALLOWED_EXTENSIONS = {
    # Images
    'png', 'jpg', 'jpeg', 'webp', 'svg', 
    # Documents
    'pdf', 'doc', 'docx'
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file_extension(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file_size: int) -> bool:
    return file_size <= MAX_FILE_SIZE