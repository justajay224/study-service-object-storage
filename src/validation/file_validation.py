from typing import List

# validasi jenis file
def validate_file_extension(filename: str, allowed_extensions: List[str] = ['png', 'jpg', 'jpeg', 'pdf']) -> bool:
    extension = filename.split('.')[-1].lower()
    return extension in allowed_extensions

# validasi ukuran
def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> bool:
    return file_size <= max_size
