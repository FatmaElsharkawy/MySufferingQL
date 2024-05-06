from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.db import connection

from .forms import UserInputForm
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


# def get_user_input(request):
#     if request.method == 'POST':
#         form = UserInputForm(request.POST)
#         if form.is_valid():
#             # Process the data in form.cleaned_data
#             data = form.cleaned_data['user_data']
#             # Do something with the data
#             ...
#             return render(request, 'success.html')  # Redirect after POST
#     else:
#         form = UserInputForm()  # An unbound form

#     return render(request, 'input_form.html', {'form': form})

from django.db import connection
from django.contrib.auth.hashers import check_password

# def authenticate_user(request):
#     # Create a new database cursor
#         if request.method == 'POST':
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#         with connection.cursor() as cursor:
#         # Execute the raw SQL query
#             cursor.execute("SELECT * FROM users WHERE email = %s", [email])
#             user = cursor.fetchone()

#         # Check if a user with the provided email exists
#             if user:
#             # user[5] is the index of the password field
#                 hashed_password = user[5]
            
#             # Use Django's check_password method to compare the passwords
#                 if check_password(password, hashed_password):
#                 # Password is correct, return the user object
#                     return HttpResponse('Welcome Back')
#                 else:
#                 # Password is incorrect
#                     return HttpResponseNotFound('Password is incorrect')
#             else:
#             # No user found with the provided username
#                 return HttpResponseNotFound("User doesn't exist")

from django.db import connection
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.hashers import check_password

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
            hashed_password = user[6]

            # Use Django's check_password method to compare the passwords
            if check_password(password, hashed_password):
                # Password is correct, return the user object
                return HttpResponse('Welcome Back')
            else:
                # Password is incorrect
                return HttpResponse(f"Entered Password: {password} and Database Password: {hashed_password}")
        else:
            # No user found with the provided email
            return HttpResponseNotFound("User doesn't exist")


from django.shortcuts import render, redirect
# from .models import User
from django.contrib.auth.hashers import make_password

# def create_user(request):
#     email = "hashtest@gmail.com"
#     raw_password = '12345'  # Get the raw password

#         # Hash the password
#     hashed_password = make_password(raw_password)

#         # Create a new user
#     sql = "INSERT INTO users (fname, lname, email, address, phone_number, password) VALUES ('hash','test', %s, '123 Street', '010', %s)"
#     with connection.cursor() as cursor:
#         cursor.execute(sql, [email, hashed_password])
#         connection.commit()
#     # user = User(fname = 'hash', lname='test',address='123 Street', phone_number='010', email=email, password=hashed_password)
#     # user.save()
#     return HttpResponse("Temporary user created") # Render your registration form template


# # Usage
# user = authenticate_user('my_username', 'my_password')
# if user:
#     print("User authenticated successfully!")
# else:
#     print("Authentication failed.")

