from django.contrib import admin

# Register your models here.
from .models import Typewriter, Textdata, Message


admin.site.register(Textdata)
admin.site.register(Message)

class TypewriterAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = [field.name for field in model._meta.fields]

# Register the Typewriter model with the TypewriterAdmin class
admin.site.register(Typewriter, TypewriterAdmin)