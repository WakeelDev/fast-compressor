# Install:
# pip install fastapi uvicorn pillow python-multipart

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from PIL import Image

import io
import os
import tempfile
import zipfile
import uuid

# --------------------------------------------------
# App Initialization
# --------------------------------------------------

app = FastAPI(
    title="FastCompress Image Engine",
    description="Privacy-first image compression API",
    version="1.0.0"
)

# Allow frontend (Vercel) to communicate with backend (Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict later to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024      # 5 MB per image
MAX_FILES_BATCH = 10                # Prevent abuse
DEFAULT_QUALITY = 65
MIN_QUALITY = 30
MAX_QUALITY = 85

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def process_image_logic(input_bytes: bytes, quality: int) -> bytes:
    """
    Compress image bytes into WebP format.
    """
    img = Image.open(io.BytesIO(input_bytes)).convert("RGB")
    output_buffer = io.BytesIO()
    img.save(
        output_buffer,
        format="WEBP",
        quality=quality,
        method=6
    )
    return output_buffer.getvalue()


def remove_tmp(path: str):
    """
    Remove temporary files safely.
    """
    if os.path.exists(path):
        os.remove(path)

# --------------------------------------------------
# Health Check (Important for Render)
# --------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "ok"}

# --------------------------------------------------
# Image Compression Endpoint
# --------------------------------------------------

@app.post("/compress/images")
async def compress_images(
    background_tasks: BackgroundTasks,
    files: list[UploadFile] = File(...),
    quality: int = DEFAULT_QUALITY
):
    # Validate batch size
    if not files or len(files) > MAX_FILES_BATCH:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {MAX_FILES_BATCH} images allowed per request"
        )

    # Clamp quality safely
    quality = max(MIN_QUALITY, min(MAX_QUALITY, quality))

    temp_dir = tempfile.gettempdir()

    # --------------------------------------------------
    # Single Image
    # --------------------------------------------------
    if len(files) == 1:
        file = files[0]

        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 5MB)")

        compressed_data = process_image_logic(content, quality)

        tmp_path = os.path.join(temp_dir, f"{uuid.uuid4()}.webp")
        with open(tmp_path, "wb") as f:
            f.write(compressed_data)

        background_tasks.add_task(remove_tmp, tmp_path)

        return FileResponse(
            tmp_path,
            media_type="image/webp",
            filename="compressed.webp"
        )

    # --------------------------------------------------
    # Multiple Images (ZIP)
    # --------------------------------------------------
    zip_path = os.path.join(temp_dir, f"batch_{uuid.uuid4()}.zip")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            if file.content_type not in ALLOWED_TYPES:
                continue  # Skip unsupported files silently

            content = await file.read()
            if len(content) > MAX_FILE_SIZE:
                continue  # Skip oversized files

            compressed_data = process_image_logic(content, quality)

            base_name = os.path.splitext(file.filename)[0]
            zipf.writestr(f"{base_name}.webp", compressed_data)

    background_tasks.add_task(remove_tmp, zip_path)

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="compressed_images.zip"
    )

# --------------------------------------------------
# Local Development Only
# --------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
