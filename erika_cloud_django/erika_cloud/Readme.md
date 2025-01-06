# Erika Cloud Backend

Django-based backend service for Erika typewriters cloud connectivity.

## Quick Start

### Using Docker (Recommended)

1. Clone the repository
2. Create `.env` file with required environment variables:
```bash
# Required environment variables
MQTT_HOST=your_mqtt_host
MQTT_PORT=1883  
MQTT_USER=your_mqtt_user
MQTT_PASS=your_mqtt_password

# Optional Django config
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=password
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

3. Start the services:
```bash
docker-compose up -d
```

### This will start:

* Django web server on port 8111
* PostgreSQL database
* Adminer (DB management) on port 8080
### Local Development
1. Install dependencies:
2. Run Migration:
```bash
python manage.py migrate
```
3. Create superuser:
```bash
python manage.py createsuperuser
```
4. Run the server:
```bash
python manage.py runserver
```
5. Start MQTT client:
```bash
poetry run python manage.py mqtt
```
## Architecture
The application consists of:

* Django web server handling HTTP requests
* MQTT client for real-time communication with typewriters
* PostgreSQL database for persistence

### License
MIT