from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from typewriter.utils.mqtt_utils import send_print_message
from .models import Typewriter, Textdata, Message
from django.views.decorators.http import require_POST
import json

@login_required
def user_dashboard(request):
    typewriter_id = request.GET.get('typewriter_id')
    print(f"Got typewriter_id: {typewriter_id}")
    
    typewriters = Typewriter.objects.filter(user=request.user)
    print(f"Found typewriters: {typewriters.count()}")
    
    context = {
        'typewriters': typewriters,
        'selected_typewriter': None,
        'messages': [],
        'pages': []
    }
    
    if not typewriter_id and typewriters.exists():
        # Auto-select first typewriter if none selected
        typewriter_id = typewriters.first().id
        print(f"Auto-selected typewriter_id: {typewriter_id}")
    
    if typewriter_id and typewriters.exists():
        selected_typewriter = typewriters.filter(id=typewriter_id).first()
        print(f"Selected typewriter: {selected_typewriter}")
        
        if selected_typewriter:
            context['selected_typewriter'] = selected_typewriter
            context['messages'] = Message.objects.filter(typewriter=selected_typewriter).order_by('-received_at')  # Changed from -timestamp
            
            # Get all textdata grouped by hashid
            textdata_groups = {}
            textdata = Textdata.objects.filter(typewriter=selected_typewriter).order_by('-timestamp', 'hashid')
            print(f"Found {textdata.count()} textdata entries")
            
            for text in textdata:
                print(f"Processing hashid: {text.hashid}")
                if text.hashid not in textdata_groups:
                    line_count = Textdata.objects.filter(
                        typewriter=selected_typewriter,
                        hashid=text.hashid
                    ).count()
                    
                    textdata_groups[text.hashid] = {
                        'text': Textdata.as_fulltext(text.hashid),  # Changed: calling as class method
                        'timestamp': text.timestamp,
                        'hashid': text.hashid,
                        'line_count': line_count  # Add line count here
                    }
            
            context['pages'] = list(textdata_groups.values())

    return render(request, 'user_dashboard.html', context)


@require_POST
@login_required
def print_page(request, typewriter_id):
    data = json.loads(request.body)
    hashid = data.get('hashid')
    
    typewriter = get_object_or_404(Typewriter, id=typewriter_id, user=request.user)
    text = Textdata.as_fulltext(hashid)
    
    if text:
        send_print_message(typewriter.uuid, text)
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def page_content(request, hashid):
    page_data = Textdata.objects.filter(hashid=hashid).first()
    if not page_data:
        return JsonResponse({'error': 'Page not found'}, status=404)
        
    content = {
        'text': Textdata.as_fulltext(hashid),
        'timestamp': page_data.timestamp.strftime("%Y-%m-%d %H:%M"),
        'hashid': hashid,
        'typewriter_uuid': page_data.typewriter.uuid
    }
    return JsonResponse(content)


