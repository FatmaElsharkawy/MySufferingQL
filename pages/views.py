from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404

# Create your views here.

def index(request):
    return render(request, "pages/register.html")
