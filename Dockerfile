# Gunakan versi Python 3.10 yang ringan sebagai dasar
FROM python:3.11-slim

# Tentukan direktori kerja di dalam container
WORKDIR /app

# Install dependensi sistem operasi (wajib untuk OpenCV dan manipulasi gambar)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Salin file requirements terlebih dahulu untuk optimasi cache Docker
COPY requirements.txt .

# Install semua pustaka Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh file kode (seperti main.py) ke dalam container
COPY . .

# Beri tahu Docker bahwa aplikasi ini berjalan di port 8000
EXPOSE 8000

# Perintah untuk menyalakan server FastAPI saat container berjalan
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]