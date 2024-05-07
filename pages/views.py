from django.db import connection
from django.shortcuts import render, redirect

# Create your views here.

x= {'name':'laila khaled mohamed', 'age':123456789}
def index(request):
  return render(request, 'pages/index.html', x)
def about(request):
  return render(request, 'pages/about.html', x)
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