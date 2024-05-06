from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.db import connection
from django.contrib.auth.hashers import check_password

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

def authenticate_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Execute the raw SQL query to fetch the user by email
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", [email])
            user = cursor.fetchone()

        if user:
            # user[6] is the index of the password field
            hashed_password = user[6] #change it so the 6 is not hardcoded

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


