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
    return render(request, "pages/login.html")

def test_db(request): #DELETE
    with connection.cursor() as cursor:
        cursor.execute('SELECT * from users')
        data = cursor.fetchall()
    return render(request, 'pages/test_db.html',{'data': data})

from django.shortcuts import render
from .forms import UserInputForm

def get_user_input(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            data = form.cleaned_data['user_data']
            # Do something with the data
            ...
            return render(request, 'success.html')  # Redirect after POST
    else:
        form = UserInputForm()  # An unbound form

    return render(request, 'input_form.html', {'form': form})
