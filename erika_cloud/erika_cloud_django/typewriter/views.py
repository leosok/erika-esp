from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Typewriter, Textdata, Message


@login_required
def user_dashboard(request):
    typewriters = Typewriter.objects.filter(user=request.user)

    if typewriters.exists():
        # If a specific typewriter is selected, use that. Otherwise, use the first one.
        selected_typewriter_id = request.GET.get('typewriter_id')
        if selected_typewriter_id:
            selected_typewriter = typewriters.filter(id=selected_typewriter_id).first()
        else:
            selected_typewriter = typewriters.first()

        pages = Textdata.as_fulltext(hashid=selected_typewriter.uuid)
        messages = Message.objects.filter(typewriter=selected_typewriter)
    else:
        selected_typewriter = None
        pages = ""
        messages = []

    context = {
        'typewriters': typewriters,
        'selected_typewriter': selected_typewriter,
        'pages': pages,
        'messages': messages,
    }
    return render(request, 'user_dashboard.html', context)