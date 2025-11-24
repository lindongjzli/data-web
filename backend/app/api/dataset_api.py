import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, concurrency
from starlette.responses import FileResponse
from starlette.background import BackgroundTask

from app.services.security_service import get_current_active_user
from app.core.config import DATASET_PATH

router = APIRouter()

@router.get("/info")
async def get_dataset_info():
    """
    Provides public information about the dataset.
    """
    return {
        "title": "交通基础设施病害数据集",
        "description": "该数据集包含了多种常见交通基础设施（如道路、桥梁）的表面病害图像，每张图像都配有详细的JSON文件，描述了病害的类型、位置和严重程度。该数据集旨在为计算机视觉研究（特别是目标检测和图像分割）提供高质量的训练和测试数据。",
        "version": "1.0.0",
        "author": "（您的姓名或团队名）",
        "citation": "（请在此处填写您的论文引用信息）",
        "file_types": ["JPG Images", "JSON Metadata"],
    }

@router.get("/download")
async def download_dataset(current_user: dict = Depends(get_current_active_user)):
    """
    Allows authenticated users to download the dataset as a ZIP file.
    This version is improved to handle cleanup correctly and avoid blocking.
    """
    # Ensure the data directory exists
    if not os.path.isdir(DATASET_PATH):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Dataset directory not found on server.")

    source_folder = os.path.join(DATASET_PATH, "dataset_source")
    if not os.path.isdir(source_folder):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source dataset folder not found on server.")

    # Define paths for the temporary ZIP file
    zip_filename = f"dataset_{current_user['username']}.zip"
    temp_zip_path = os.path.join(DATASET_PATH, zip_filename)
    base_zip_name = os.path.splitext(temp_zip_path)[0]
    
    try:
        # Run the blocking I/O operation in a separate thread pool
        await concurrency.run_in_threadpool(
            shutil.make_archive, base_name=base_zip_name, format='zip', root_dir=source_folder
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create archive: {e}")

    # Check if the file was created before attempting to send it
    if not os.path.exists(temp_zip_path):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create or find the dataset archive.")

    # Create a background task to clean up the temporary file AFTER the response is sent
    cleanup_task = BackgroundTask(os.remove, temp_zip_path)

    return FileResponse(
        path=temp_zip_path,
        filename="TIDD_dataset_v1.zip",
        media_type='application/zip',
        background=cleanup_task
    )