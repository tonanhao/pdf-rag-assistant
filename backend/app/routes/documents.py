from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from typing import List
import os
from pathlib import Path
import uuid
import shutil

from ..config import BASE_DIR, UPLOAD_DIR

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Check if the file is a PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Generate a unique filename
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{file_id}{file_extension}"
    file_path = UPLOAD_DIR / file_name
    
    # Save the file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    return {
        "id": file_id,
        "filename": file.filename,
        "stored_filename": file_name,
        "path": str(file_path)
    }

@router.get("/{file_id}")
async def get_document(file_id: str):
    # Look for files with the given ID (regardless of extension)
    matching_files = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    
    if not matching_files:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = matching_files[0]
    return FileResponse(path=file_path, filename=file_path.name)

@router.delete("/{file_id}")
async def delete_document(file_id: str):
    # Look for files with the given ID (regardless of extension)
    matching_files = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    
    if not matching_files:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = matching_files[0]
    os.remove(file_path)
    
    return JSONResponse(content={"message": "Document deleted successfully"}) 