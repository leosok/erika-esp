import logging
from dmqtt.signals import connect, topic
from django.dispatch import receiver
from django.conf import settings

# Configure logger
logger = logging.getLogger('mqtt_handler')


@receiver(connect)
def on_connect(sender, **kwargs):
    logger.info(f"MQTT Configuration - Host: {settings.MQTT_HOST}, Port: {settings.MQTT_PORT}, "
            f"User: {settings.MQTT_USER}, Password set: {bool(settings.MQTT_PASS)}")

    # Subscribe to wildcard first, then specific topic
    topics_to_subscribe = ["erika/#", "erika/print/all"]
    for sub_topic in topics_to_subscribe:
        sender.subscribe(sub_topic)
        logger.info(f"MQTT Connected and subscribed to topic: {sub_topic}")


@topic("erika/print/all", as_json=False)
def simple_topic(sender, topic, msg, **kwargs):
    try:
        payload = msg.payload.decode("utf8")
        logger.info(f"MQTT message received on topic: {topic} with payload: {payload}")
    except Exception as e:
        logger.error(f"Error processing MQTT message on topic: {topic} - Error: {str(e)}")
