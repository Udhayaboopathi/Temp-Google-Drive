# File Management System - Self-Hosted Cloud Storage

A complete full-stack file management application similar to Google Drive, built with FastAPI and vanilla JavaScript.

## Features

- 📁 **Folder Organization** - Create and manage folders
- 📤 **File Upload** - Drag-and-drop or click to upload files
- 📥 **Downloads** - Single file or bulk ZIP downloads
- 🎬 **Media Preview** - Play videos and audio directly in browser
- 🖼️ **File Type Support** - Videos, audio, images, PDFs, and more
- 📱 **Responsive Design** - Works on desktop and mobile
- 🔒 **Security** - Input validation and path traversal protection

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Storage**: Local filesystem

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the repository**

2. **Install Python dependencies**

```bash
cd backend
pip install -r requirements.txt
```

3. **Run the backend server**

```bash
python main.py
```

The backend will start at `http://localhost:8000`

4. **Open the frontend**

- Open `frontend/index.html` in your web browser
- Or serve it using a simple HTTP server:

```bash
cd frontend
python -m http.server 3000
```

Then navigate to `http://localhost:3000`

## Usage

### File Operations

- **Upload Files**: Drag and drop files or click the upload button
- **Create Folders**: Click "New Folder" and enter a folder name
- **Navigate**: Click on folders to open them, use breadcrumb navigation to go back
- **Preview**: Click on video/audio files to play them in the browser
- **Download**: Click download button on individual files
- **Bulk Download**: Select multiple files and click "Download Selected as ZIP"
- **Delete**: Click delete button on files/folders (with confirmation)

### Supported File Types

- **Videos**: mp4, webm, avi, mov, mkv
- **Audio**: mp3, wav, ogg, m4a, aac
- **Images**: jpg, jpeg, png, gif, bmp, svg
- **Documents**: pdf, txt, doc, docx
- **Archives**: zip, rar, tar, gz
- **Others**: All other file types can be uploaded and downloaded

## API Endpoints

### Files

- `POST /api/upload` - Upload files
- `GET /api/files` - List files in folder
- `GET /api/download/{file_path}` - Download single file
- `POST /api/download-zip` - Download multiple files as ZIP
- `DELETE /api/files/{file_path}` - Delete file
- `GET /api/stream/{file_path}` - Stream video/audio

### Folders

- `POST /api/folders` - Create folder
- `DELETE /api/folders/{folder_path}` - Delete folder

## Configuration

### File Upload Limits

Edit `backend/main.py` to change the maximum file size (default: 1GB):

```python
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
    maximum_size=1024 * 1024 * 1024  # 1GB
)
```

### Storage Location

Files are stored in `backend/storage/` by default. You can change this in `backend/main.py`:

```python
STORAGE_DIR = Path("storage")
```

## Security Features

- ✅ Path traversal prevention
- ✅ File name validation
- ✅ Folder name validation
- ✅ CORS configuration
- ✅ Safe file handling
- ✅ Input sanitization

## Development

### Backend Development

```bash
cd backend
uvicorn main:app --reload
```

### Frontend Development

The frontend is a single-page application with no build process required. Simply edit `frontend/index.html` and refresh your browser.

## Troubleshooting

### CORS Errors

Make sure the backend is running and CORS is properly configured in `main.py`.

### File Upload Fails

- Check file size limits
- Ensure the `storage/` directory has write permissions
- Check available disk space

### Preview Not Working

- Ensure your browser supports HTML5 video/audio
- Check that the file format is supported by your browser
- Verify the backend streaming endpoint is accessible

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

```

```
