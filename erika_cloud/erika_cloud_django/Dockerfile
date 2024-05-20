# the Dockerfile to start django
# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONPATH "${PYTHONPATH}:/app"

# we need to install poetry to install the dependencies
RUN pip install poetry

# Copy the poetry.lock and pyproject.toml to the container
COPY pyproject.toml poetry.lock ./

# Install the dependencies
RUN poetry install

# Copy the Django project to the container
COPY . .

# Expose the port that Django runs on
EXPOSE 8111

# Start the Django development server, we use 8111 to avoid conflict with the host

# pause the container for debugging
#CMD ["sleep", "240"]

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8111"]