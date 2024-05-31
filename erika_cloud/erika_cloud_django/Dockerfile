# the Dockerfile to start django
# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

RUN pip install poetry

# Copy the poetry.lock and pyproject.toml to the container
COPY pyproject.toml poetry.lock ./

# Configure Poetry to create the virtual environment inside the project directory
# RUN poetry config virtualenvs.in-project true

# Install the dependencies
RUN poetry install --without dev --no-root

##### End of dependencies installation #####

COPY . .

# Ensure the .venv bin directory is on the PATH environment variable
# ENV PATH="/app/.venv/bin:$PATH"

# Expose the port that Django runs on
EXPOSE 8111

# create a superuser
#RUN poetry run python manage.py createsuperuser --noinput --username admin --email admin@example.com

CMD ["poetry", "run", "python3", "manage.py", "runserver", "0.0.0.0:8111"]