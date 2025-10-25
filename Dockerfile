# Use official Python image
FROM python:3.10-slim

# Set work directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    pip install --upgrade pip

# Copy all project files into container
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt

# Expose Django's port
EXPOSE 8000

# Command to run the app
CMD ["bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

