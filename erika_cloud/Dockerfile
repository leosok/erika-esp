# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run models.py to create the models
RUN python models.py

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run Super User Creation from .env
RUN poetry run python manage.py createsuperuser --noinput

# Run the app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "bottle_app:application"]