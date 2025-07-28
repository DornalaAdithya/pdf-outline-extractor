# Use a lightweight Python base image
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY main.py .

# Define input/output folders as Docker volumes
VOLUME ["/app/input", "/app/output"]

# Default command to run your script
CMD ["python", "main.py"]