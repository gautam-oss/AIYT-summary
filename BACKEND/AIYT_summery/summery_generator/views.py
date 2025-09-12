from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.shortcuts import redirect,render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_login(request):
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        usename = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        if password == repeatPassword:
            try:
                from django.contrib.auth.models import User
                user = User.objects.create_user(usename, email, password)
                user.save()
                return redirect('login')
            except:
                error_message = "error in creating user"
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = "Password and Repeat Password do not match"
            return render(request, 'signup.html', {'error_message': error_message})
            
        
    return render(request, 'signup.html')   

def user_logout(request):
    pass