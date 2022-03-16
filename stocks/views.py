from distutils import errors
from django.shortcuts import render
from .forms import LoginForm, RegisterForm, ResetForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    context = {"day":20092021}
    return render(request, 'stocks/index.html', context)

def login_auth(request):
    if request.method == "POST" :
        if 'login_button' in request.POST :
            form = LoginForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                password = form.cleaned_data['password']
                user = authenticate(request, username=user, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    response = redirect('/')
                    return response
            else:
                print(form.errors)
        if 'register_button' in request.POST :
            form = RegisterForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.create_user(name, email,password)
                response = redirect('/confirmation')
                return response
            else: 
                f = {'form':form}
                return render(request, 'stocks/register.html', context=f)
        if 'reset_button_confirmation' in request.POST:
            form = ResetForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data['email'])
            else:
                print(form.errors)
            return render(request, 'stocks/reset.html')
        if 'reset_button_cancellation' in request.POST:
            return render(request, 'stocks/login.html')
    return render(request, 'stocks/login.html')

def logout_view(request):
    logout(request)   
    response = redirect('/')
    return response

def register(request):
    if request.method == "GET":
        return render(request, 'stocks/register.html')
    if request.method == "POST":
        if 'register_button' in request.POST :
            form = RegisterForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.create_user(name, email,password)
                response = redirect('/confirmation')
                return response
            else: 
                f = {'form':form}
                return render(request, 'stocks/register.html', context=f)
        if 'login_button' in request.POST :
            form = LoginForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                password = form.cleaned_data['password']
                user = authenticate(request, username=user, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    response = redirect('/')
                    return response
            else:
                print(form.errors)
            return render(request, 'stocks/login.html')
        if 'reset_button_confirmation' in request.POST:
            form = ResetForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data['email'])
            else:
                print(form.errors)
            return render(request, 'stocks/reset.html')
        if 'reset_button_cancellation' in request.POST:
            return render(request, 'stocks/login.html')
    
def confirmation(request):
    if request.method == "GET":
        return render(request, 'stocks/confirmation.html')
    if request.method == "POST":
        response = redirect('/')
        return response
        
def account(request):
    return render(request, 'stocks/account.html')

def edit(request):
    return render(request, 'stocks/edit.html')

def reset(request):
    return render(request, 'stocks/reset.html')

def list(request):
    return render(request, 'stocks/list.html')

def daydetails(request, date):
    return render(request, 'stocks/daydetails.html')

def stock(request, stockname):
    context = {"name":stockname}
    return render(request, 'stocks/stock.html',context )