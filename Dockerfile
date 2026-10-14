FROM python:3.11-slim

WORKDIR /app

# Install dependensi sistem
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Perbarui pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install PyTorch versi stabil terlebih dahulu agar tidak error
RUN pip install --no-cache-dir torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cpu

# Install sisa pustaka dari requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode
COPY . .

# Jalankan aplikasi dengan port dinamis Render
CMD uvicorn main:app --host 0.0.0.0 --port $PORT