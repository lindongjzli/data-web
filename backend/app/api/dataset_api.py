import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

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
    """
    # Ensure the data directory exists
    if not os.path.isdir(DATASET_PATH):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset directory not found on server.")

    # For simplicity, we assume the data is in a folder named 'dataset_source' inside the DATASET_PATH
    source_folder = os.path.join(DATASET_PATH, "dataset_source")
    if not os.path.isdir(source_folder):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source dataset not found on server.")

    # Create a temporary ZIP file
    zip_filename = f"dataset_{current_user['username']}.zip"
    temp_zip_path = os.path.join(DATASET_PATH, zip_filename)
    
    print(f"Zipping folder {source_folder} to {temp_zip_path}...")
    shutil.make_archive(os.path.splitext(temp_zip_path)[0], 'zip', source_folder)
    print("Zipping complete.")

    # Send the file and clean up afterwards
    return FileResponse(
        path=temp_zip_path,
        filename="TIDD_dataset_v1.zip",
        media_type='application/zip',
        background=os.remove(temp_zip_path) # Delete the temp file after sending
    )
