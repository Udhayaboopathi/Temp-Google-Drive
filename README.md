# 📂 File Management System

<div align="center">

**A Beautiful, Modern Self-Hosted Cloud Storage Solution**

_Built with FastAPI & Vanilla JavaScript - No Framework Bloat!_

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Demo](#-screenshots) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-documentation)

</div>

---

## ✨ Features

### 🎨 **Modern Dark UI**

- Stunning purple & cyan dark theme
- Smooth animations and transitions
- Responsive grid and list views
- Mobile-friendly design

### � **Complete File Management**

- ✅ Create nested folders
- ✅ Drag & drop file upload
- ✅ Bulk file operations
- ✅ Context menu (right-click)
- ✅ Breadcrumb navigation
- ✅ Select all functionality

### 🎬 **Rich Media Support**

- **Video**: MP4, WebM, AVI, MOV, MKV - Play in-browser
- **Audio**: MP3, WAV, OGG, M4A - Built-in player
- **Images**: JPG, PNG, GIF, BMP, SVG - Preview
- **Documents**: PDF viewer, Text files
- **Archives**: ZIP, RAR, TAR, GZ

### 🚀 **Advanced Features**

- Real-time file streaming
- Bulk ZIP download
- File type detection
- Progress notifications
- Keyboard shortcuts (ESC to close)
- Animated loading states

### 🔒 **Security Built-In**

- Path traversal protection
- Input validation & sanitization
- Safe file name handling
- CORS configuration
- XSS prevention

## 🛠️ Tech Stack

| Component        | Technology                                          |
| ---------------- | --------------------------------------------------- |
| **Backend**      | Python 3.8+, FastAPI, Uvicorn                       |
| **Frontend**     | HTML5, CSS3 (Custom Properties), Vanilla JavaScript |
| **Storage**      | Local Filesystem                                    |
| **Architecture** | REST API                                            |

## 📦 Installation

### Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- **pip** (usually comes with Python)
- A modern web browser (Chrome, Firefox, Safari, Edge)

### Quick Start

#### 1️⃣ Clone or Download

```bash
git clone <your-repository-url>
cd files
```

#### 2️⃣ Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Dependencies installed:**

- `fastapi` - Modern web framework
- `uvicorn[standard]` - ASGI server
- `python-multipart` - File upload support
- `aiofiles` - Async file operations

#### 3️⃣ Start the Backend

```bash
python main.py
```

**Output:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### 4️⃣ Open the Frontend

**Option A - Direct File (Simple)**

```bash
# Just open the file in your browser
open frontend/index.html  # macOS
xdg-open frontend/index.html  # Linux
start frontend/index.html  # Windows
```

**Option B - HTTP Server (Recommended)**

```bash
cd frontend
python -m http.server 3000
```

Then visit: `http://localhost:3000`

🎉 **Done!** Your file management system is running!

---

## 🎯 Usage

### Basic Operations

#### 📤 Upload Files

1. **Drag & Drop**: Drag files from your computer directly to the upload area
2. **Click to Browse**: Click the "Choose Files" button
3. **Multiple Files**: Select multiple files at once

#### 📁 Create Folders

1. Click **"📁 New Folder"**
2. Enter folder name
3. Press **Enter** or click **"Create"**

#### 🔽 Navigate Folders

- **Click folder** to open
- **Breadcrumb navigation** to go back
- **Home icon** (🏠) to return to root

#### 👁️ Preview Media

- **Videos/Audio**: Click "▶️ Play" button
- **Images**: Click "👁️ View" button
- **PDFs**: Opens in built-in viewer
- **Close**: Press **ESC** or click "Close"

#### 💾 Download Files

- **Single File**: Click download button on any file
- **Multiple Files**:
  1. Select files using checkboxes
  2. Click **"📦 Download Selected as ZIP"**

#### 🗑️ Delete Files/Folders

- **Single Item**: Click delete button (confirms before deletion)
- **Multiple Items**:
  1. Select items using checkboxes
  2. Click **"🗑️ Delete Selected"**

#### 🖱️ Context Menu (Right-Click)

Right-click on any file or folder for quick actions:

- Open (folders)
- Preview (media files)
- Download (files)
- Delete

### View Modes

- **🔲 Grid View**: Visual card layout (default)
- **📄 List View**: Compact table layout

### Keyboard Shortcuts

| Key     | Action                           |
| ------- | -------------------------------- |
| `ESC`   | Close modal/preview/context menu |
| `Enter` | Confirm folder creation          |

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api
```

### Endpoints

#### 📤 **Upload Files**

```http
POST /api/upload
Content-Type: multipart/form-data

files: File[]
folder: string (optional, current folder path)
```

**Response:**

```json
{
  "message": "Files uploaded successfully",
  "files": ["file1.jpg", "file2.pdf"]
}
```

---

#### 📋 **List Files**

```http
GET /api/files?folder={path}

Parameters:
  - folder: string (optional, defaults to root)
```

**Response:**

```json
{
  "folders": [
    {
      "name": "Documents",
      "path": "Documents",
      "modified": "2025-10-30T12:00:00"
    }
  ],
  "files": [
    {
      "name": "image.jpg",
      "path": "image.jpg",
      "size": 102400,
      "type": "image",
      "modified": "2025-10-30T12:00:00"
    }
  ]
}
```

---

#### 💾 **Download Single File**

```http
GET /api/download/{file_path}

Parameters:
  - file_path: URL-encoded file path
```

**Response:** File download

---

#### 📦 **Download Multiple Files as ZIP**

```http
POST /api/download-zip
Content-Type: application/json

{
  "files": ["file1.jpg", "folder/file2.pdf"]
}
```

**Response:** ZIP file download

---

#### 🎬 **Stream Media**

```http
GET /api/stream/{file_path}

Parameters:
  - file_path: URL-encoded file path
```

**Response:** Media stream (video/audio)

---

#### 📁 **Create Folder**

```http
POST /api/folders
Content-Type: application/json

{
  "name": "New Folder",
  "current_path": "parent/path"  // optional
}
```

**Response:**

```json
{
  "message": "Folder created successfully",
  "path": "parent/path/New Folder"
}
```

---

#### 🗑️ **Delete File**

```http
DELETE /api/files/{file_path}

Parameters:
  - file_path: URL-encoded file path
```

**Response:**

```json
{
  "message": "File deleted successfully"
}
```

---

#### 🗑️ **Delete Folder**

```http
DELETE /api/folders/{folder_path}

Parameters:
  - folder_path: URL-encoded folder path
```

**Response:**

```json
{
  "message": "Folder deleted successfully"
}
```

---

## ⚙️ Configuration

### Change Upload Limit

Edit `backend/main.py`:

```python
# Current: 1GB limit
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB

# Change to 500MB
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
```

### Change Storage Directory

```python
# Default
STORAGE_DIR = Path("storage")

# Custom location
STORAGE_DIR = Path("/path/to/your/storage")
```

### Change Server Port

```python
# In main.py, bottom of file
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)  # Changed to 8080
```

### Customize Theme Colors

Edit `frontend/index.html` CSS variables:

```css
:root {
  --primary-color: #8b5cf6; /* Purple accent */
  --secondary-color: #06b6d4; /* Cyan accent */
  --bg-color: #0f172a; /* Dark background */
  --card-bg: #1e293b; /* Card background */
  /* ... customize as needed */
}
```

---

## 🔧 Troubleshooting

### ❌ CORS Errors

**Problem:** Frontend can't connect to backend

**Solution:**

```python
# In backend/main.py, ensure:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ❌ Upload Fails

**Problem:** Files won't upload

**Check:**

1. ✅ Backend server is running (`http://localhost:8000`)
2. ✅ `backend/storage/` directory exists and is writable
3. ✅ File size is under limit (default 1GB)
4. ✅ Sufficient disk space

**Fix permissions (Linux/Mac):**

```bash
chmod -R 755 backend/storage
```

### ❌ Media Won't Play

**Problem:** Videos/audio won't preview

**Possible causes:**

- Browser doesn't support the codec
- File is corrupted
- Backend streaming endpoint not accessible

**Solution:**

- Try converting to MP4 (video) or MP3 (audio)
- Check browser console for errors
- Ensure backend is running

### ❌ Port Already in Use

**Problem:** `Address already in use`

**Solution:**

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :8000   # Windows (find PID, then kill)

# Or change port in main.py
```

---

## 🎨 Screenshots

### Grid View (Dark Theme)

_Beautiful card layout with file type icons and hover effects_

### List View

_Compact table view for power users_

### Media Preview

_Built-in video/audio player and image viewer_

---

## 🗂️ Project Structure

```
files/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── storage/            # File storage directory
│       └── (your files here)
├── frontend/
│   └── index.html          # Single-page application
├── README.md               # This file
└── .gitignore             # Git ignore rules
```

---

## 🚀 Advanced Usage

### Run in Production

```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Run as Service (Linux)

Create `/etc/systemd/system/filemanager.service`:

```ini
[Unit]
Description=File Management System
After=network.target

[Service]
User=youruser
WorkingDirectory=/path/to/files/backend
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl enable filemanager
sudo systemctl start filemanager
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
EXPOSE 8000
CMD ["python", "main.py"]
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Feature Ideas

- 🔍 Search functionality
- 🔐 User authentication
- 📊 Storage analytics
- 🎨 Light/Dark theme toggle
- 📱 Mobile app
- ☁️ Cloud storage integration

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can use this for personal or commercial projects, modify it, distribute it - just keep the copyright notice.

---

## 🙏 Acknowledgments

- **FastAPI** - Amazing Python web framework
- **Uvicorn** - Lightning-fast ASGI server
- Built with ❤️ by developers, for developers

---

## 📞 Support

- 🐛 **Bug Reports**: Open an issue
- 💡 **Feature Requests**: Open an issue with `enhancement` label
- 💬 **Questions**: Discussions section

---

<div align="center">

**Made with ❤️ and ☕**

If you found this helpful, give it a ⭐!

[⬆ Back to Top](#-file-management-system)

</div>
