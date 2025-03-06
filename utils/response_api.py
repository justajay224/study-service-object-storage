from typing import List, Dict

def generate_response(metaData: Dict = None, data: List = None) -> Dict:
    # Default jika metaData atau data tidak diberikan
    metaData = metaData or {}
    data = data or []
    
    # Default values 
    code = metaData.get('code', 500)
    message = metaData.get('message', 'Ok')
    res_code = metaData.get('response_code', '0001')

    response = {
        'response': data,
        'metaData': {
            'message': message,
            'code': code,
            'response_code': '0000' if code == 200 else res_code
        }
    }
    
    return response

def generate_error_response(message: str, code: int, response_code: str) -> Dict:
    meta_data = {
        'message': message,
        'code': code,
        'response_code': response_code
    }
    return generate_response(metaData=meta_data, data=[])
