from utils.response_api import generate_error
import base64

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov', "mkv"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB

# Validasi untuk endpoint upload
def validate_upload_request(filename: str, file_data: str):
    if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return generate_error("Invalid file extension", 400, "0001")
    
    try:
        decoded_data = base64.b64decode(file_data)
    except Exception:
        return generate_error("Invalid base64", 400, "0003")
    
    if len(decoded_data) == 0:
        return generate_error("File data is empty", 400, "0005")
    
    if len(decoded_data) > MAX_FILE_SIZE:
        return generate_error("File too large", 400, "0002")
    
    return None

# Validasi untuk endpoint update
def validate_update_request(filename: str, file_data: str):
    if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return generate_error("Invalid file extension", 400, "0007")
    
    try:
        decoded_data = base64.b64decode(file_data)
    except Exception:
        return generate_error("Invalid base64", 400, "0008")
    
    if len(decoded_data) == 0:
        return generate_error("File data is empty", 400, "0005")
    
    if len(decoded_data) > MAX_FILE_SIZE:
        return generate_error("File too large", 400, "0002")
    
    return None