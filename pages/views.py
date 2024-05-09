from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection, transaction
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password


# Create your views here.
def index(request):
    # Clearing session and cookies
    request.session.flush()
    request.session.modified = True
    
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
                        INSERT INTO useraccount (Fname,Lname, Email, passward, address, phone, gender)
                        VALUES (%s, %s, %s,%s, %s, %s, %s);
                    """, [first_name, last_name, email, password, address, phone_number, gender]) 
                    # Getting user ID
            with connection.cursor() as cursor:
                cursor.execute("""SELECT id
                               FROM useraccount
                               WHERE email = %s""", [email])
                id = cursor.fetchone()
            request.session['id'] = id
            ### Opening profiel
            return redirect('profile')
        else:
            return HttpResponse('''Password is incorrect.''')
    return render(request, "pages/register.html")

def login(request):
    return render(request, "pages/login.html")

def authenticate_user(request):
    # Clearing session and cookies
    request.session.flush()
    request.session.modified = True

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Getting user ID
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id
                           FROM useraccount
                           WHERE email = %s""", [email])
            id = cursor.fetchone()

        if id:    
            # Execute the raw SQL query to fetch the user by id
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM useraccount WHERE id = %s", [id])
                user = cursor.fetchone()
                # user[5] is the index of the password field
            hashed_password = user[4] #change it so the 5 is not hardcoded

                # Use Django's check_password method to compare the passwords
            if password == hashed_password:
                # Password is correct, return the user object
                request.session['id'] = id
                return render(request, 'pages/profile.html', {'loginfo':user})
            else:
                # Password is incorrect
                error_message = "The password you entered is incorrect."
                return render(request, 'pages/login.html', {'error_message': error_message})
        else:
            # No user found with the provided email
            error_message = "This user does not exist. Please check your email or sign up for a new account."
            return render(request, 'pages/login.html', {'error_message': error_message})    

def profile(request):
    id = request.session.get('id')
    if id:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM useraccount WHERE id = %s", [id[0]])
            result1 = cursor.fetchone()
            cursor.execute("SELECT * FROM social WHERE id = %s", [id[0]])
            result2 = cursor.fetchone()
        return render(request, 'pages/profile.html', {'loginfo':result1,
                                                      'acc': result2}) 
    return HttpResponse("Email not found in session.")

# Editing user accounts
def edit(request):
    id = request.session.get('id')
    if id:
        if request.method == 'POST':
            fb = request.POST.get('fb')
            ins = request.POST.get('ins')
            ln = request.POST.get('ln')
            git = request.POST.get('git')
            with connection.cursor() as cursor:
                cursor.execute("""SELECT id
                                FROM social
                                WHERE id = %s""", [id[0]])
                result = cursor.fetchone()
                if result is None: result = ['dummy']
            res = [0]
            for i in range(len(result)):
                res[i] = result[i]
            if id[0] in result:
                with connection.cursor() as cursor:
                    cursor.execute("""UPDATE social
                                    SET facebook = %s, instagram = %s, linkedin = %s, github = %s
                                    WHERE id = %s""", [fb, ins, ln, git, id[0]])
            else:
                with connection.cursor() as cursor:
                    cursor.execute("""INSERT INTO social
                                    (id, facebook, github, instagram, linkedin)
                                    VALUES(%s, %s, %s, %s, %s)""",[id[0], fb, git, ins, ln])
            transaction.commit()
            return redirect('profile')
    return render(request, 'pages/edit.html')

# Editing user info
def editinfo(request):
    id = request.session.get('id')
    if id:
        if request.method == 'POST':
            first = request.POST.get('first')
            last = request.POST.get('last')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            add = request.POST.get('add')

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE useraccount
                                SET fname = %s, lname = %s, email = %s, phone = %s, address = %s
                                WHERE id = %s""", [first, last, email, phone, add, id[0]])
            transaction.commit()
            return redirect('profile')
    return render(request, 'pages/editinfo.html')