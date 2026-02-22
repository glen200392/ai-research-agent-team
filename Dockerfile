FROM python:3.11-slim

# System deps for playwright and other tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create output directories
RUN mkdir -p reports tmp/pipeline pedagogy/weekly-lessons

# Default: show help
ENTRYPOINT ["python", "run.py"]
CMD ["--help"]
