from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import List, Optional
import shutil
import os
from datetime import datetime
import mimetypes
import zipfile
from io import BytesIO
import re
from pydantic import BaseModel

app = FastAPI(title="File Management System")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage directory
STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)

# Security: Validate file/folder names
def sanitize_path(name: str) -> str:
    """Remove dangerous characters and prevent path traversal"""
    # Remove any path traversal attempts
    name = name.replace("..", "").replace("/", "").replace("\\", "")
    # Remove leading/trailing spaces and dots
    name = name.strip(". ")
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"|?*\x00-\x1f]', '', name)
    if not name:
        raise ValueError("Invalid name")
    return name

def validate_path(path: Path) -> Path:
    """Ensure path is within storage directory"""
    try:
        resolved = path.resolve()
        storage_resolved = STORAGE_DIR.resolve()
        if not str(resolved).startswith(str(storage_resolved)):
            raise HTTPException(status_code=400, detail="Invalid path")
        return resolved
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid path")

class FolderCreate(BaseModel):
    name: str
    current_path: str = ""

class FileDelete(BaseModel):
    path: str

class DownloadZipRequest(BaseModel):
    files: List[str]

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main index.html page"""
    html_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(html_path)

@app.post("/api/upload")
async def upload_file(
    files: List[UploadFile] = File(...),
    folder: str = Form("")
):
    """Upload one or more files to specified folder"""
    try:
        # Sanitize folder path
        folder_path = STORAGE_DIR
        if folder:
            folder_parts = [sanitize_path(part) for part in folder.split("/") if part]
            folder_path = STORAGE_DIR / "/".join(folder_parts)
            folder_path.mkdir(parents=True, exist_ok=True)
        
        validate_path(folder_path)
        
        uploaded_files = []
        for file in files:
            # Sanitize filename
            safe_filename = sanitize_path(file.filename)
            file_path = folder_path / safe_filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_files.append({
                "name": safe_filename,
                "path": str(file_path.relative_to(STORAGE_DIR))
            })
        
        return {
            "message": f"Successfully uploaded {len(uploaded_files)} file(s)",
            "files": uploaded_files
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/api/files")
async def list_files(folder: str = ""):
    """List all files and folders in specified directory"""
    try:
        # Build folder path
        folder_path = STORAGE_DIR
        if folder:
            folder_parts = [sanitize_path(part) for part in folder.split("/") if part]
            folder_path = STORAGE_DIR / "/".join(folder_parts)
        
        validate_path(folder_path)
        
        if not folder_path.exists():
            return {"files": [], "folders": []}
        
        files = []
        folders = []
        
        for item in folder_path.iterdir():
            if item.is_file():
                stat = item.stat()
                # Determine file type
                mime_type, _ = mimetypes.guess_type(item.name)
                file_type = "other"
                if mime_type:
                    if mime_type.startswith("video/"):
                        file_type = "video"
                    elif mime_type.startswith("audio/"):
                        file_type = "audio"
                    elif mime_type.startswith("image/"):
                        file_type = "image"
                    elif mime_type == "application/pdf":
                        file_type = "pdf"
                
                files.append({
                    "name": item.name,
                    "path": str(item.relative_to(STORAGE_DIR)),
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "type": file_type,
                    "mime_type": mime_type or "application/octet-stream"
                })
            elif item.is_dir():
                stat = item.stat()
                folders.append({
                    "name": item.name,
                    "path": str(item.relative_to(STORAGE_DIR)),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        # Sort: folders first, then files, both alphabetically
        folders.sort(key=lambda x: x["name"].lower())
        files.sort(key=lambda x: x["name"].lower())
        
        return {"files": files, "folders": folders}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

@app.post("/api/folders")
async def create_folder(folder_data: FolderCreate):
    """Create a new folder"""
    try:
        # Sanitize folder name
        safe_name = sanitize_path(folder_data.name)
        
        # Build full path
        base_path = STORAGE_DIR
        if folder_data.current_path:
            path_parts = [sanitize_path(part) for part in folder_data.current_path.split("/") if part]
            base_path = STORAGE_DIR / "/".join(path_parts)
        
        new_folder_path = base_path / safe_name
        validate_path(new_folder_path)
        
        if new_folder_path.exists():
            raise HTTPException(status_code=400, detail="Folder already exists")
        
        new_folder_path.mkdir(parents=True)
        
        return {
            "message": "Folder created successfully",
            "name": safe_name,
            "path": str(new_folder_path.relative_to(STORAGE_DIR))
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create folder: {str(e)}")

@app.get("/api/download/{file_path:path}")
async def download_file(file_path: str):
    """Download a single file"""
    try:
        # Sanitize and validate path
        path_parts = [sanitize_path(part) for part in file_path.split("/") if part]
        full_path = STORAGE_DIR / "/".join(path_parts)
        validate_path(full_path)
        
        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=full_path,
            filename=full_path.name,
            media_type="application/octet-stream"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.post("/api/download-zip")
async def download_zip(request: DownloadZipRequest):
    """Download multiple files as a ZIP archive"""
    try:
        if not request.files:
            raise HTTPException(status_code=400, detail="No files specified")
        
        # Create ZIP file in memory
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in request.files:
                # Sanitize and validate each path
                path_parts = [sanitize_path(part) for part in file_path.split("/") if part]
                full_path = STORAGE_DIR / "/".join(path_parts)
                validate_path(full_path)
                
                if full_path.exists() and full_path.is_file():
                    # Add file to ZIP with its relative path
                    zip_file.write(full_path, arcname=full_path.name)
        
        zip_buffer.seek(0)
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=files.zip"}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ZIP creation failed: {str(e)}")

@app.get("/api/download-folder/{folder_path:path}")
async def download_folder(folder_path: str):
    """Download entire folder as a ZIP archive"""
    try:
        # Sanitize and validate path
        path_parts = [sanitize_path(part) for part in folder_path.split("/") if part]
        full_path = STORAGE_DIR / "/".join(path_parts)
        validate_path(full_path)
        
        if not full_path.exists() or not full_path.is_dir():
            raise HTTPException(status_code=404, detail="Folder not found")
        
        # Create ZIP file in memory
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Walk through directory and add all files
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    file_full_path = Path(root) / file
                    # Create archive name preserving folder structure
                    arcname = file_full_path.relative_to(full_path)
                    zip_file.write(file_full_path, arcname=str(arcname))
        
        zip_buffer.seek(0)
        
        # Use folder name for ZIP filename
        folder_name = full_path.name or "folder"
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={folder_name}.zip"}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Folder download failed: {str(e)}")

@app.get("/api/stream/{file_path:path}")
async def stream_file(file_path: str):
    """Stream video/audio/image/PDF files for preview"""
    try:
        # Sanitize and validate path
        path_parts = [sanitize_path(part) for part in file_path.split("/") if part]
        full_path = STORAGE_DIR / "/".join(path_parts)
        validate_path(full_path)
        
        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(full_path.name)
        if not mime_type:
            mime_type = "application/octet-stream"
        
        # Return file with inline disposition for browser viewing
        with open(full_path, "rb") as f:
            content = f.read()
        
        return Response(
            content=content,
            media_type=mime_type,
            headers={
                "Content-Disposition": f'inline; filename="{full_path.name}"'
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stream failed: {str(e)}")

@app.delete("/api/files/{file_path:path}")
async def delete_file(file_path: str):
    """Delete a file"""
    try:
        # Sanitize and validate path
        path_parts = [sanitize_path(part) for part in file_path.split("/") if part]
        full_path = STORAGE_DIR / "/".join(path_parts)
        validate_path(full_path)
        
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        if full_path.is_file():
            full_path.unlink()
        else:
            raise HTTPException(status_code=400, detail="Not a file")
        
        return {"message": "File deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

@app.delete("/api/folders/{folder_path:path}")
async def delete_folder(folder_path: str):
    """Delete a folder and all its contents"""
    try:
        # Sanitize and validate path
        path_parts = [sanitize_path(part) for part in folder_path.split("/") if part]
        full_path = STORAGE_DIR / "/".join(path_parts)
        validate_path(full_path)
        
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="Folder not found")
        
        if full_path.is_dir():
            shutil.rmtree(full_path)
        else:
            raise HTTPException(status_code=400, detail="Not a folder")
        
        return {"message": "Folder deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)