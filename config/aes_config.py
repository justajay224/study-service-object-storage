import os
import base64
from dotenv import load_dotenv

load_dotenv()

KEY_BASE64 = os.getenv("ENCRYPTION_KEY")
if not KEY_BASE64:
    raise ValueError("Key must be set in the .env file")

try:
    KEY = base64.b64decode(KEY_BASE64)
except base64.binascii.Error:
    raise ValueError("Key is not a valid Base64 string")

if len(KEY) != 32:
    raise ValueError("Key must be 32 bytes long after decoding")