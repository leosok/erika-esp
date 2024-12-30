import logging

from ninja import NinjaAPI, Swagger, Router

from erika_cloud import settings

# rewrite swagger to have try out button automatically enabled
api = NinjaAPI(csrf=True, title="Erika Cloud", version="1.0.0", docs=Swagger(settings={"tryItOutEnabled": True}))

router = Router()
# add health check endpoint
@router.get("/healthz")
def healthz(request):
    return {"status": "ok"}


def send_password_reset_email(email_adresse):
    pass


@router.get("/test_mail")
def sent_test_mail(request, email_adresse: str):
    # Log the email credentials
    logging.info(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    logging.info(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    logging.info(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    logging.info(f"EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD}")

    send_password_reset_email(email_adresse)
    return {"detail": "Test email sent successfully"}
