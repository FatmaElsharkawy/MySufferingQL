from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.db import connection
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('number')
        address = request.POST.get('address')
        email = request.POST.get('email')
        raw_password = request.POST.get('password')
        raw_password_2 = request.POST.get('confirm-password')
        gender = request.POST.get('gender')

        if confirm_password(raw_password,raw_password_2):
            password= make_password('raw_password')
            with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO "profile" (Fname,Lname, Email, passward, address, phone, gender)
                        VALUES (%s, %s, %s,%s, %s, %s, %s);
                    """, [first_name, last_name, email, password, address, phone_number, gender])
            return HttpResponse('''<h1> Successfully Registered </h1>''')
        else:
            return HttpResponse('''<h1> Password is incorrect </h1>''')
    return render(request, "pages/register.html")

def login(request):
    pass
'''
def success(request):
    return render(request, "pages/success.html")
'''
def confirm_password(raw_password,raw_password_2):
    if raw_password is raw_password_2:
        return True
    else:
        return False
