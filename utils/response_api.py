from fastapi.responses import JSONResponse

def generate_success(data: dict, message: str, code: int, response_code: str = "0000") -> JSONResponse:
    return JSONResponse(
        content={
            "data": data,
            "metaData": {
                "message": message,
                "code": code,
                "response_code": response_code
            }
        },
        status_code=code
    )


def generate_error(message: str, code: int, response_code: str) -> JSONResponse:
    return JSONResponse(
        content={
            "data": None,
            "metaData": {
                "message": message,
                "code": code,
                "response_code": response_code
            },
        },
        status_code=code
    )
