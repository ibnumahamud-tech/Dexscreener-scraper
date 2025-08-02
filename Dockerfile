FROM python:3.9-slim

# 1) Set working dir
WORKDIR /usr/src/app

# 2) Copy requirements and install
COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy your app code
COPY api .

# 4) Tell Docker how to run it
CMD ["python", "main.py"]
