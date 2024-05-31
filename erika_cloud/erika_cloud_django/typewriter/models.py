from django.utils import timezone
from django.db import models

class Textdata(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    hashid = models.CharField(max_length=255)
    line_number = models.IntegerField()

    @classmethod
    def count_lines(cls, hashid):
        return cls.objects.filter(hashid=hashid).count()

    @classmethod
    def as_fulltext(cls, hashid, min_length=30):
        lines = cls.objects.filter(hashid=hashid).order_by('line_number')
        fulltext = ''
        for line in lines:
            if len(line.content) <= min_length:
                fulltext += line.content + '\n'
            else:
                fulltext += line.content + ' '
        return fulltext

class Typewriter(models.Model):
    user_firstname = models.CharField(max_length=255, null=True)
    user_lastname = models.CharField(max_length=255, null=True)
    erika_name = models.CharField(max_length=255, null=True, unique=True)
    user_email = models.CharField(max_length=255, null=True)
    uuid = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)
    chat_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(default=timezone.now)

class Message(models.Model):
    typewriter = models.ForeignKey(Typewriter, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    received_at = models.DateTimeField(default=timezone.now)
    is_printed = models.BooleanField(default=False)