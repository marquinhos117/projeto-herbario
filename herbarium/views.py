# herbarium/views.py
from django.shortcuts import render

def home(request):
    # Por enquanto, apenas renderiza o template
    return render(request, 'herbarium/pages/home.html')