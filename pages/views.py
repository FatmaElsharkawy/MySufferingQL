from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.db import connection
# Create your views here.

def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS USER (
                id SERIAL PRIMARY KEY,
                Name VARCHAR(50),
                email VARCHAR(50),
                Password VARCHAR(20),
            );
        """)

def index(request):
    return render(request, "pages/register.html")

def login(request):
    pass
