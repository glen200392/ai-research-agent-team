FROM python:3.11-slim

# System utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Create runtime output directories
RUN mkdir -p reports tmp/pipeline pedagogy/weekly-lessons \
             docs/evolution-chronicle/by-period \
             docs/evolution-chronicle/by-technology

# Install and configure the dual-mode entrypoint
COPY docker-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# API server port (used when START_MODE=api)
EXPOSE 8080

# Default: CLI mode — run `python run.py <args>`
# Override with START_MODE=api for the FastAPI server
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["--help"]
