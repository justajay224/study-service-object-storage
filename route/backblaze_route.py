from fastapi import APIRouter, UploadFile, File
from src.controller.backblaze_controller import BackblazeController

router = APIRouter()

backblaze_controller = BackblazeController()

router.add_api_route("/upload", backblaze_controller.upload_file, methods=["POST"])
router.add_api_route("/files", backblaze_controller.list_files, methods=["GET"])
