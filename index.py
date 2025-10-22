# Use official Python image
FROM python:3.10-slim

# Install MeCab + dependencies
RUN apt-get update && apt-get install -y \
    mecab libmecab-dev mecab-ipadic-utf8 git curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Render expects
EXPOSE 10000

# Run your Flask app
CMD ["python", "index.py"]
