# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install Poetry
RUN pip install poetry

# Configure Poetry to create the virtual environment inside the project directory
RUN poetry config virtualenvs.in-project true

# Install dependencies
RUN poetry install --no-root

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run Super User Creation from .env
RUN poetry run python manage.py createsuperuser --noinput

# Run the app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "bottle_app:application"]