from ninja import NinjaAPI, Swagger

api = NinjaAPI()

from django.contrib import admin
from django.urls import path
from .api import api

# rewrite swagger to have try out button automatically enabled
api = NinjaAPI(csrf=True, title="Erika Cloud", version="1.0.0", docs=Swagger(settings={"tryItOutEnabled": True}))


@api.get("/hello")
def hello(request):
    return "Hello world"

# add health check endpoint
@api.get("/healthz")
def healthz(request):
    return {"status": "ok"}