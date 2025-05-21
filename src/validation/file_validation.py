ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov'}
MAX_FILE_SIZE = 25 * 1024 * 1024  

def validate_file_extension(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file_size: int) -> bool:
    return file_size <= MAX_FILE_SIZE