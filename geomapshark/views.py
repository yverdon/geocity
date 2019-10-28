from django.shortcuts import render
from . import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.views.static import serve

@login_required
def index(request):

    apps = {
        'yvent': settings.YVENT_URL,
        'mapnv': settings.MAPNV_URL,
        'signalez': settings.SIGNALEZ_URL,
    }
    context = { 'apps': apps }

    return render(request, 'geomapshark/index.html', context)

@login_required
def protected_serve(request, path, document_root=None):
    return serve(request, path, document_root)
