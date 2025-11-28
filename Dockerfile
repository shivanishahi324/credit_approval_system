# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc ca-certificates && \
    update-ca-certificates && \
    pip install --upgrade pip

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose Render port
EXPOSE 10000

# Start app with migrations + Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn credit_approval.wsgi:application --bind 0.0.0.0:10000"]

