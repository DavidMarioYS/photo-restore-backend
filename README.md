# AI Photo Restoration - Backend (FastAPI) 🧠📸

This is the backend service for the AI Photo Restoration project. It provides a robust REST API built with FastAPI that leverages state-of-the-art Deep Learning models to restore old, blurry, or degraded photographs.

## 🚀 Features

- **Face Restoration:** Utilizes **GFPGAN** to recover realistic facial details from heavily degraded images.
- **Background Enhancement:** Uses **Real-ESRGAN** for general image super-resolution and background noise removal.
- **FastAPI Framework:** Ensures high performance, automatic documentation (Swagger UI), and easy endpoint management.
- **CORS Enabled:** Ready to be consumed by modern web frontends.
- **Docker-Ready:** (Optional) Prepared for containerized deployment.

## 🛠️ Tech Stack

- **Python 3**
- **FastAPI** & **Uvicorn**
- **PyTorch**
- **GFPGAN** & **Real-ESRGAN**
- **OpenCV** & **NumPy**

## endpoint API

### `POST /restore`
Accepts a degraded image file and returns the restored image as a binary blob.
- **Content-Type:** `multipart/form-data`
- **Body:** `file` (image)
- **Response:** `image/jpeg` or `image/png`

## 💻 Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/photo-restore-backend.git
   cd photo-restore-backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

## ⚠️ Notes
Image processing relies heavily on CPU/GPU. If running locally without a dedicated GPU, processing a single image may take a few minutes.