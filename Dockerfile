# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN cd visitor_portal && python manage.py collectstatic --noinput || true

# Run migrations
RUN cd visitor_portal && python manage.py migrate || true

# Expose port
EXPOSE 8000

# Run gunicorn
CMD cd visitor_portal && gunicorn visitor_portal.wsgi:application --bind 0.0.0.0:8000

