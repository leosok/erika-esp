import datetime
import logging
from dmqtt.signals import connect, topic
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from typewriter.models import Textdata, Typewriter

# Configure logger
logger = logging.getLogger('mqtt_handler')

@receiver(connect)
def on_connect(sender, **kwargs):
    logger.info(f"MQTT Configuration - Host: {settings.MQTT_HOST}, Port: {settings.MQTT_PORT}, "
            f"User: {settings.MQTT_USER}, Password set: {bool(settings.MQTT_PASS)}")

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
        
@topic("erika/status/+", as_json=False)
def handle_status(sender, topic, msg, **kwargs):
    logger.info(f"MQTT message received on topic: {topic} with payload: {msg.payload}")
    try:
        typewriter_id = topic.split('/')[2]
        status = int(msg.payload)
        logger.info(f"Status of Typewriter {typewriter_id} changed to {status}")
        try:
            typewriter = Typewriter.objects.get(uuid=typewriter_id)
            if typewriter.status < status:
                typewriter.print_mails()
            typewriter.status = status
            typewriter.save()
        except Typewriter.DoesNotExist:
            logger.info(f"Typewriter not found: {typewriter_id=}")
    except Exception as e:
        logger.error(f"Error processing status message: {str(e)}")

@topic("erika/upload/#", as_json=True)
def handle_upload(sender, topic, msg, **kwargs):
    logger.info(f"MQTT message received on topic: {topic} with payload: {msg.payload}")
    try:
        if "cmd" in msg and msg["cmd"] == "email":
            subject = f'Erika Text {datetime.datetime.now().strftime("%d.%m.%Y")}'
            content = Textdata.as_fulltext(msg['hashid'])
            send_mail(
                subject=subject,
                message=content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[msg['to']],
                fail_silently=False,
            )
        else:
            Textdata.objects.create(
                content=msg['line'],
                hashid=msg['hashid'],
                line_number=msg['lnum']
            )
    except Exception as e:
        logger.error(f"Error processing upload message: {str(e)}")
