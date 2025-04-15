from pydantic import BaseModel
from typing import Optional

# Model untuk Response
class ResponseModel(BaseModel):
    fileId: Optional[str]
    fileName: Optional[str]
    message: Optional[str]
    status: Optional[str]

# Model untuk MetaData
class MetaDataModel(BaseModel):
    message: str
    code: int
    response_code: str

# Model untuk format Response lengkap
class ApiResponse(BaseModel):
    response: ResponseModel
    metaData: MetaDataModel
