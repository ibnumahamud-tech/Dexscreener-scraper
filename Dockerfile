FROM python:3.9-slim

# 1) Set working dir
WORKDIR /usr/src/app

# 2) Copy the root requirements.txt (not under api/)
COPY requirements.txt ./

# 3) Install deps
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy all of the api/ folder into the container
COPY api/ ./

# 5) Launch your Flask app directly (assuming you renamed app.py → main.py)
CMD ["python", "main.py"]
