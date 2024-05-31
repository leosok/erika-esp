from django.contrib import admin

# Register your models here.
from .models import Typewriter, Textdata, Message

admin.site.register(Typewriter)
admin.site.register(Textdata)
admin.site.register(Message)
