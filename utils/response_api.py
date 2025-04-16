from fastapi.responses import JSONResponse

def generate_success(data: dict, message: str, code: int, response_code: str = "0000") -> JSONResponse:
    return JSONResponse(
        content={
            "metaData": {
                "message": message,
                "code": code,
                "response_code": response_code
            },
            "data": data
        },
        status_code=code
    )

def generate_error(message: str, code: int, response_code: str) -> JSONResponse:
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
    
# Response Code	HTTP Status	Pesan	Konteks Penggunaan
# 0000	200/201	OK / Success	Operasi berhasil (default untuk semua success)
# 0001	400	Invalid file extension	Ekstensi file tidak diizinkan saat upload
# 0002	400	File too large	Ukuran file melebihi batas maksimal (10MB)
# 0003	400	Invalid base64	Data base64 tidak valid saat upload
# 0004	500	[Pesan error server]	Gagal upload file ke Backblaze
# 0005	500	[Pesan error server]	Gagal download file dari Backblaze
# 0006	500	[Pesan error server]	Gagal mengambil daftar file
# 0007	400	Invalid file extension	Ekstensi file tidak valid saat update file
# 0008	400	Invalid base64	Data base64 tidak valid saat update file
# 0009	500	[Pesan error server]	Gagal update file di Backblaze
# 0010 500 [Pesan error server] Gagal menghapus file di Backblaze
# 0010 404 File not found File tidak ditemukan saat menghapus
