import json

import paho.mqtt.client as mqtt
import logging
import time
from django.conf import settings

logger = logging.getLogger(__name__)


def send_print_message(uuid: str, message: str) -> None:
    """
    Send a print message to a specific typewriter

    Args:
        uuid: The typewriter's UUID
        message: The message to send (will be converted to string)
    """
    # Create a new MQTT client
    client = mqtt.Client()

    uuid = None

    # Track connection and publish status
    is_connected = False
    is_published = False

    # Set credentials
    client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASS)

    # Debugging connection details
    print(f"Connecting to MQTT broker at {settings.MQTT_HOST}:{settings.MQTT_PORT} "
                f"as {settings.MQTT_USER}")

    # Define event callbacks for better debugging
    def on_connect(client, userdata, flags, rc):
        nonlocal is_connected
        if rc == 0:
            is_connected = True
            logger.info("MQTT client connected successfully.")
            print(f"Connected with result code {rc}")
        else:
            logger.error(f"MQTT connection failed with code {rc}.")
            print(f"Connection failed with code {rc}")

    def on_publish(client, userdata, mid):
        nonlocal is_published
        is_published = True
        logger.info(f"Message published successfully: {mid}")
        print(f"Message published with mid {mid}")

    client.on_connect = on_connect
    client.on_publish = on_publish

    # Connect to the broker
    try:
        client.connect(host=settings.MQTT_HOST,
                       port=settings.MQTT_PORT,
                       keepalive=60)
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        print(f"Failed to connect to MQTT broker: {e}")
        return

    # Start the loop
    client.loop_start()

    # Wait for connection
    timeout = time.time() + 5  # 5 second timeout
    while not is_connected and time.time() < timeout:
        time.sleep(0.1)

    if not is_connected:
        logger.error("Failed to connect to MQTT broker (timeout)")
        client.loop_stop()
        client.disconnect()
        return

    # Format topic and message
    topic = f"erika/print/{uuid or 'all'}"

    if "all" in topic:
        message = json.dumps(
            {
                "text": message,
                "sender": "erika_cloud"
            }
        )


    logger.info(f"Publishing message to {topic}: {message}")
    print(f"Publishing message to {topic}: {message}")

    # Publish and wait for confirmation
    client.publish(topic, str(message), qos=1)

    # Wait for publish confirmation
    timeout = time.time() + 5  # 5 second timeout
    while not is_published and time.time() < timeout:
        time.sleep(0.1)

    # Give a small delay to ensure message is fully sent
    time.sleep(0.5)

    # Stop the loop and disconnect
    client.loop_stop()
    client.disconnect()

    if is_published:
        logger.info("Message successfully published and client disconnected.")
        print("Message successfully published and client disconnected.")
    else:
        logger.error("Failed to publish message (timeout)")
        print("Failed to publish message (timeout)")