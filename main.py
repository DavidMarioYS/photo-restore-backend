import cv2
import numpy as np
import io
import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse

# Import pustaka restorasi
from gfpgan import GFPGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SISR & Face Restoration API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Inisialisasi Model Real-ESRGAN (Untuk memperbaiki latar belakang & resolusi)
# Menggunakan arsitektur RRDBNet standar
model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
bg_upsampler = RealESRGANer(
    scale=2,
    model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
    model=model,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=False # Ubah ke True jika nanti menggunakan GPU untuk optimasi memori
)

# 2. Inisialisasi Model GFPGAN (Untuk restorasi wajah rusak/buram)
face_enhancer = GFPGANer(
    model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
    upscale=2, # Target upscale resolusi 2x lipat
    arch='clean',
    channel_multiplier=2,
    bg_upsampler=bg_upsampler
)

@app.post("/restore")
async def restore_photo(file: UploadFile = File(...)):
    # 3. Ekstraksi gambar biner ke format array NumPy untuk pemrosesan OpenCV
    image_bytes = await file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 4. Eksekusi Inferensi AI
    # GFPGAN mengembalikan tuple: (cropped_faces, restored_faces, restored_img)
    # Kita hanya mengambil output akhir (elemen ketiga)
    _, _, restored_img = face_enhancer.enhance(
        img, 
        has_aligned=False, 
        only_center_face=False, 
        paste_back=True
    )

    # Fallback pencegahan error jika wajah gagal dideteksi
    if restored_img is None:
        restored_img = img

    # 5. Konversi balik dari array ke JPEG dan kirim sebagai StreamingResponse
    _, encoded_img = cv2.imencode('.jpg', restored_img)
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)