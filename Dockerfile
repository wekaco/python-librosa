FROM python:3.7-slim

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    sndfile-tools \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
   pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "/bin/sh" ]
