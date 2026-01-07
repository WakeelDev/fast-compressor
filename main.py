# Install: pip install fastapi uvicorn pillow python-multipart
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import io, os, tempfile, zipfile, uuid
from PIL import Image

app = FastAPI(title="FastCompress Image Engine")

# This allows your local HTML file to talk to the Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_image_logic(input_bytes, quality=65):
    img = Image.open(io.BytesIO(input_bytes)).convert('RGB')
    out_buf = io.BytesIO()
    # Saves as WebP for maximum compression and site speed
    img.save(out_buf, format='WEBP', quality=quality, method=6)
    return out_buf.getvalue()

def remove_tmp(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.post("/compress/images")
async def compress_images(background_tasks: BackgroundTasks, files: list[UploadFile] = File(...)):
    if len(files) == 1:
        file = files[0]
        content = await file.read()
        compressed_data = process_image_logic(content)
        
        tmp_name = f"{uuid.uuid4()}.webp"
        with open(tmp_name, "wb") as f:
            f.write(compressed_data)
        
        background_tasks.add_task(remove_tmp, tmp_name)
        return FileResponse(tmp_name, media_type="image/webp", filename="compressed.webp")
    else:
        zip_filename = f"batch_{uuid.uuid4()}.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in files:
                content = await file.read()
                compressed_data = process_image_logic(content)
                zipf.writestr(f"{file.filename.split('.')[0]}.webp", compressed_data)
        
        background_tasks.add_task(remove_tmp, zip_filename)
        return FileResponse(zip_filename, media_type="application/zip", filename="images.zip")

if __name__ == "__main__":
    import uvicorn
    # Use 127.0.0.1 for local testing to avoid the 0.0.0.0 error
    uvicorn.run(app, host="127.0.0.1", port=8000)