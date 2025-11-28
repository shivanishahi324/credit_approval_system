# Use official Python image
FROM python:3.10-slim

# Set work directory inside the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    ca-certificates && \
    update-ca-certificates && \
    pip install --upgrade pip

# Copy project files
COPY . /app/

# Very Important: Copy SQLite DB for free hosting
COPY db.sqlite3 /app/db.sqlite3

# Install dependencies
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose Render's port
EXPOSE 10000

# Start Django + run migrations (SQLite)
CMD ["sh", "-c", "python manage.py migrate && gunicorn credit_approval.wsgi:application --bind 0.0.0.0:10000"]
