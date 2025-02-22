FROM python:3.9

# Install dependencies yang dibutuhkan untuk OpenCV, MediaPipe, dan PyAutoGUI
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libx11-6 \
    x11-utils \
    xserver-xorg \
    x11-xserver-utils \
    xdg-utils \
    libxkbcommon-x11-0 \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Salin file requirements.txt dan install dependency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode ke dalam container
COPY . .

# Jalankan program
CMD ["python", "main.py"]
