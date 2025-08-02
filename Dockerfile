FROM python:3.9-slim

# Install build tools so misaka’s C extension can compile
RUN apt-get update \
 && apt-get install -y gcc libffi-dev python3-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copy and install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your scraper code
COPY api/ ./

# Run your app
CMD ["python", "main.py"]
