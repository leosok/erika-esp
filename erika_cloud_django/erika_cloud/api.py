import logging

from ninja import NinjaAPI, Swagger, Router
from django.core.mail import send_mail

from erika_cloud import settings

# rewrite swagger to have try out button automatically enabled
api = NinjaAPI(csrf=True, title="Erika Cloud", version="1.0.0", docs=Swagger(settings={"tryItOutEnabled": True}))

router = Router()
# add health check endpoint
@router.get("/healthz")
def healthz(request):
    return {"status": "ok"}


@router.get("/test_email_just_django")
def send_test_email1(request, to_email: str = "l.sokolov@gmx.de"):
        # Log the email credentials
    logging.info(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    logging.info(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    logging.info(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    logging.info(f"EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD}")


    send_mail(
        subject="Test Email",
        message="Hello from Erika Cloud!",
        from_email="no-reply@erika-cloud.de",  # or settings.DEFAULT_FROM_EMAIL
        recipient_list=[to_email],
        fail_silently=False,
    )
    return {"detail": "Email sent!"}
