# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables securely
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

WORKDIR $APP_HOME

# Install dependencies safely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py .

# Create a non-root application user for safety
RUN useradd -m appuser && chown -R appuser:appuser $APP_HOME
USER appuser

# Expose microservice port
EXPOSE 8000

# Execute the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]