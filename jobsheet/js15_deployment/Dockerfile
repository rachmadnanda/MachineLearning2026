# Base image Python 3.12 slim
FROM python:3.12-slim

# Library sistem untuk OpenCV headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# User non-root (standar keamanan Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
ENV TF_CPP_MIN_LOG_LEVEL=3

WORKDIR /app

# Install dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy aplikasi & artefak model
COPY --chown=user . /app

EXPOSE 7860
CMD ["python", "app.py"]