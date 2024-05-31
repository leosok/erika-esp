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
    uuid = models.CharField(max_length=255, unique=True)
    user_firstname = models.CharField(max_length=255, blank=True)
    user_lastname = models.CharField(max_length=255, blank=True)
    user_email = models.EmailField()
    chat_active = models.BooleanField(default=False)
    erika_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    status = models.IntegerField(default=0)

class Message(models.Model):
    typewriter = models.ForeignKey(Typewriter, related_name='messages', on_delete=models.CASCADE)
    sender = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
