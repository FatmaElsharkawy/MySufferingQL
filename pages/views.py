from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.db import connection
from django.contrib.auth.hashers import check_password
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
    return render(request, "pages/login.html")

def authenticate_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Execute the raw SQL query to fetch the user by email
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", [email])
            user = cursor.fetchone()

        if user:
            # user[8] is the index of the password field
            hashed_password = user[8] #change it so the 8 is not hardcoded

            # Use Django's check_password method to compare the passwords
            if check_password(password, hashed_password):
                # Password is correct, return the user object
                return HttpResponse('Welcome Back')
            else:
                # Password is incorrect
                # context = {"error" : "The password you entered is incorrect."}
                # return render(request, "../login.html", context)
                return HttpResponse("""    <div>
                                            <h1 style='color:rgb(200,0,0)'>The password you entered is incorrect.</h1>
                                            </div>""")
        else:
            # No user found with the provided email
            return HttpResponse("""    <div>
                                            <h1 style='color:rgb(200,0,0)'>This user does not exist.<br>
                                            Please check your email or sign up for a new account.</h1>
                                            </div>""")

def confirm_password(raw_password,raw_password_2):
    if raw_password is raw_password_2:
        return True
    else:
        return False

