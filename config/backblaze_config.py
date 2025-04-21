import os
from dotenv import load_dotenv

load_dotenv()

BACKBLAZE_KEY_ID = os.getenv("BACKBLAZE_KEY_ID")
BACKBLAZE_APPLICATION_KEY = os.getenv("BACKBLAZE_APPLICATION_KEY")
BACKBLAZE_BUCKET_NAME = os.getenv("BACKBLAZE_BUCKET_NAME")
