FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim-2022-11-25
ENV PYTHONUNBUFFERED=1

WORKDIR /backend/app

# Install necessary system packages
RUN apt clean && apt update && apt install -y \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U email-validator

# Copy the application code
COPY app ./

# Set the PYTHONPATH for the app
ENV PYTHONPATH=/backend
EXPOSE 9090
