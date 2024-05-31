import logging
import os
from email.utils import parseaddr

from django.db import IntegrityError
from ninja import NinjaAPI,  Router
from django.shortcuts import get_object_or_404

# from utils.mail_utils import print_on_erika
from .models import Textdata, Typewriter, Message
from .schemas import TextdataSchema, TypewriterSchema, MessageSchema, TypewriterCreateSchema
from typing import List

typewriter_router = Router(tags=["Typewriter"])

@typewriter_router.get("/pages", response=List[TextdataSchema])
def list_pages(request):
    pages = Textdata.objects.order_by('timestamp').distinct('hashid')
    return pages

@typewriter_router.get("/pages/{hashid}", response=TextdataSchema)
def single_page(request, hashid: str):
    action = request.query_params.get('action')
    if action == "delete":
        Textdata.objects.filter(hashid=hashid).delete()
        return {"detail": "Page deleted"}
    else:
        lines = Textdata.objects.filter(hashid=hashid).order_by('line_number')
        return {"lines": lines, "fulltext": Textdata.as_fulltext(hashid)}

@typewriter_router.get("/keycast/{uuid}", response=dict)
def keycast_receiver(request, uuid: str):
    MQQT_SERVER = os.getenv('MQQT_SERVER')
    MQQT_USERNAME = os.getenv('MQQT_USERNAME')
    MQQT_PASSWORD = os.getenv('MQQT_PASSWORD')
    topic_keycast = f"erika/keystrokes/{uuid}"
    topic_status = f"erika/status/{uuid}"
    return {
        "config": {
            "MQQT_SERVER": MQQT_SERVER,
            "MQQT_USERNAME": MQQT_USERNAME,
            "MQQT_PASSWORD": MQQT_PASSWORD,
            "erika_uuid": uuid,
            "topic_keycast": topic_keycast,
            "topic_status": topic_status
        }
    }

@typewriter_router.get("/erika/{uuid}/emails", response=List[MessageSchema])
def erika_single(request, uuid: str):
    typewriter = get_object_or_404(Typewriter, uuid=uuid)
    emails = typewriter.messages.all()
    return emails

@typewriter_router.get("/erika/{erika_name}", response=List[MessageSchema])
def erika_sender(request, erika_name: str):
    try:
        typewriter = Typewriter.objects.get(erika_name=erika_name.lower())
        emails = typewriter.messages.all()
        if emails.exists():
            return emails
        else:
            return {"detail": f"No messages for typewriter `{erika_name.capitalize()}`"}, 404
    except Typewriter.DoesNotExist:
        return {"detail": f"No typewriter found with name `{erika_name.capitalize()}`"}, 404

@typewriter_router.post("/incoming", response=dict)
@typewriter_router.post("/incoming_email", response=dict)
def incoming_webhook(request, data: dict):
    receiver_name, receiver_email = parseaddr(data['headers']['to'])
    sender_name, sender_email = parseaddr(data['headers']['from'])
    try:
        erika = Typewriter.objects.get(email=receiver_email.lower())
    except Typewriter.DoesNotExist:
        return {"detail": f"No Typewriter found for address {receiver_email}"}, 404

    msg = Message.objects.create(
        typewriter=erika,
        sender=sender_email,
        subject=data['headers']['subject'],
        body=data['plain']
    )

    return {"detail": "Message created"}

@typewriter_router.post("/typewriter", response=TypewriterSchema)
def register_typewriter(request, data: TypewriterCreateSchema):
    typewriter, created = Typewriter.objects.get_or_create(uuid=data.uuid)

    typewriter.user_firstname = data.firstname
    typewriter.user_lastname = data.lastname
    typewriter.user_email = data.email.lower()
    typewriter.chat_active = data.chat_active
    typewriter.erika_name = data.erika_name.lower()

    saved = False
    i = 1
    while not saved:
        try:
            typewriter.save()
            saved = True
        except IntegrityError:
            i += 1
            typewriter.erika_name = f"{data.erika_name}{i}"

    typewriter.email = f"{typewriter.erika_name.lower()}@{os.getenv('APP_HOST')}"
    typewriter.save()

    return typewriter

@typewriter_router.post("/typewriter/{uuid}/print", response=dict)
def typewriter_print(request, uuid: str, data: dict):
    logging.info("Printing")
    typewriter = get_object_or_404(Typewriter, uuid=uuid)
    #print_on_erika(typewriter, data['body'])
    return {"detail": f"Printing on `{typewriter.erika_name.capitalize()}`"}

@typewriter_router.get("/typewriters/online", response=List[TypewriterSchema])
def typewriters_online(request):
    typewriters = Typewriter.objects.filter(status=1)
    return typewriters
