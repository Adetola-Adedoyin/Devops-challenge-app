# Use a lightweight official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Set environment variable
ENV APP_ENV=production

# Expose the application port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
