from django.contrib.auth.models import User
from django.db import models

class Textdata(models.Model):
    hashid = models.CharField(max_length=255)
    line_number = models.IntegerField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def as_fulltext(hashid):
        lines = Textdata.objects.filter(hashid=hashid).order_by('line_number')
        return "\n".join([line.text for line in lines])


class Typewriter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255, unique=True)
    erika_name = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=0)
    email = models.EmailField(unique=True)
    chat_active = models.BooleanField(default=False)
    # Add other fields as necessary

class Message(models.Model):
    typewriter = models.ForeignKey(Typewriter, related_name='messages', on_delete=models.CASCADE)
    sender = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
