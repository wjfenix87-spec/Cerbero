from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .constants import FRAMEWORKS


def home(request):
    """Vista principal"""
    return render(request, 'core/home.html')

@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'ok',
        'message': 'Cerbero API funcionando 🐕',
        'version': '1.0.0'
    })

def upload_guide(request, framework):
    data = FRAMEWORKS.get(framework, FRAMEWORKS['html'])
    return render(request, 'core/upload_guide.html', {
        'framework': data,
        'framework_key': framework
    })