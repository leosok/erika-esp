from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Typewriter, Textdata, Message

@login_required
def user_dashboard(request):
    try:
        typewriter = Typewriter.objects.get(user=request.user)
        pages = Textdata.as_fulltext(hashid=typewriter.uuid)
        messages = Message.objects.filter(typewriter=typewriter)
    except Typewriter.DoesNotExist:
        typewriter = None
        pages = ""
        messages = []

    context = {
        'typewriter': typewriter,
        'pages': pages,
        'messages': messages,
    }
    return render(request, 'user_dashboard.html', context)