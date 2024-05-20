# the Dockerfile to start django
# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install poetry

# Copy the poetry.lock and pyproject.toml to the container
COPY pyproject.toml poetry.lock ./

# Install the dependencies
RUN poetry install --without dev

##### End of dependencies installation #####

COPY . .

# Expose the port that Django runs on
EXPOSE 8111

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8111"]