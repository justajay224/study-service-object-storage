from pydantic import BaseModel
from typing import Optional

# Model untuk Response (menampilkan data utama seperti file info)
class ResponseModel(BaseModel):
    fileId: Optional[str]
    fileName: Optional[str]
    message: Optional[str]
    status: Optional[str]

# Model untuk MetaData (informasi tambahan terkait status API)
class MetaDataModel(BaseModel):
    message: str
    code: int
    response_code: str

# Model untuk format Response lengkap (menggabungkan response dan metadata)
class ApiResponse(BaseModel):
    response: ResponseModel
    metaData: MetaDataModel
