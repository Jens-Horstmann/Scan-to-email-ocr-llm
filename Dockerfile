# Use a lightweight Python image
FROM python:3.11

# Install system dependencies for Tesseract and PDF processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libsm6 libxext6 poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh    

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY scan2email.py ocr.py emailer.py summarizer.py requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the scans folder (it will be mounted from the host)
RUN mkdir -p /app/scans


# Start Ollama and the script
CMD ollama serve & \
    until curl -s http://localhost:11434/api/tags > /dev/null; do sleep 2; done && \
    ollama pull qwen2.5:14b && \
    python scan2email.py
