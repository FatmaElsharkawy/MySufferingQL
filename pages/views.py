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

        if raw_password == raw_password_2:
            password= make_password('raw_password')
            with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO "profile" (Fname,Lname, Email, passward, address, phone, gender)
                        VALUES (%s, %s, %s,%s, %s, %s, %s);
                    """, [first_name, last_name, email, password, address, phone_number, gender])
            return HttpResponse('''<h1 style="align-text:center; color:rgb(0,255,0);"> Successfully Registered </h1>''')
        else:
            return HttpResponse('''Password is incorrect.''')
    return render(request, "pages/register.html")

def login(request):
    return render(request, "pages/login.html")

def authenticate_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Execute the raw SQL query to fetch the user by email
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM profile WHERE email = %s", [email])
            user = cursor.fetchone()

        if user:
            # user[5] is the index of the password field
            hashed_password = user[4] #change it so the 5 is not hardcoded

            # Use Django's check_password method to compare the passwords
            if password == hashed_password:
            #if check_password(password, hashed_password):
                # Password is correct, return the user object
                return render(request, 'pages/profile.html')
            else:
                # Password is incorrect
                # context = {"error" : "The password you entered is incorrect."}
                # return render(request, "../login.html", context)

                # return HttpResponse(f"{email}+{password}+{hashed_password}")

                return HttpResponse("""    <div>
                                            <h1 style='color:rgb(200,0,0)'>The password you entered is incorrect.</h1>
                                            </div>""")
        else:
            # No user found with the provided email
            return HttpResponse("""    <div>
                                            <h1 style='color:rgb(200,0,0)'>This user does not exist.<br>
                                            Please check your email or sign up for a new account.</h1>
                                            </div>""")

# def confirm_password(raw_password,raw_password_2):
#     if raw_password is raw_password_2:
#         return True
#     else:
#         return False

####PROFILE####

# Create your views here.

x= {'name':'laila khaled mohamed', 'age':123456789}

def profile(request):
  return render(request, 'pages/profile.html') 
def edit(request):
    if request.method == 'POST':
        fb = request.POST.get('fb', '')
        ins = request.POST.get('ins', '')
        ln = request.POST.get('ln', '')
        git = request.POST.get('git','')
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO accounts(facebook, github, instagram, linkedin)
                           VALUES(%s, %s, %s, %s)""",[fb, git, ins, ln])
        return redirect('profile')
    return render(request, 'pages/edit.html')