from pydantic import BaseModel
from typing import Optional

# Model buat Response
class ResponseModel(BaseModel):
    fileId: Optional[str]
    fileName: Optional[str]
    message: Optional[str]
    status: Optional[str]

# Model buat MetaData
class MetaDataModel(BaseModel):
    message: str
    code: int
    response_code: str

# Model buat format Response lengkap
class ApiResponse(BaseModel):
    response: ResponseModel
    metaData: MetaDataModel
