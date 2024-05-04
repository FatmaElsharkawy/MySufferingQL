from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404

# Create your views here.

def index(request):
    return HttpResponse(''' <h1> Hello to our mySufferingQL Page </h1>''' )
