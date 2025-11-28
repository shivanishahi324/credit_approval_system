# Use official Python image
FROM python:3.10-slim

# Set work directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc ca-certificates && \
    update-ca-certificates && \
    pip install --upgrade pip

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt

# Collect static files (DRF UI issue fix)
RUN python manage.py collectstatic --noinput

# Expose Render's default port
EXPOSE 10000

# Start the app:
# 1. Run migrations in PostgreSQL
# 2. Start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn credit_approval.wsgi:application --bind 0.0.0.0:10000"]

