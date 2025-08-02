FROM python:3.9-slim

# Install build tools so misaka’s C extension can compile
RUN apt-get update \
 && apt-get install -y gcc libffi-dev python3-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copy your requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the api folder INTO a subdirectory named api
COPY api ./api

# Run the actual scraper sitting at api/main.py
CMD ["python", "api/main.py"]
