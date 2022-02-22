from django.shortcuts import render
from .forms import LoginForm, RegisterForm

# Create your views here.

def index(request):
    context = {"day":20092021}
    return render(request, 'stocks/index.html', context)

def login(request):
    if request.method == "POST" :
        if 'login_button' in request.POST :
            form = LoginForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data['email'])
                print(form.cleaned_data['password'])
            else:
                print(form.errors)
        if 'register_button' in request.POST :
            form = RegisterForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data['name'])
                print(form.cleaned_data['email'])
                print(form.cleaned_data['password'])
                print(form.cleaned_data['confirm_password'])
            else:
                print(form.errors)
            return render(request, 'stocks/register.html')
    return render(request, 'stocks/login.html')
    

def register(request):
    if request.method == "POST":
        if 'register_button' in request.POST :
            form = RegisterForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data['name'])
                print(form.cleaned_data['email'])
                print(form.cleaned_data['password'])
                print(form.cleaned_data['confirm_password'])
            else:
                print(form.errors)
        if 'login_button' in request.POST :
                form = LoginForm(request.POST)
                if form.is_valid():
                    print(form.cleaned_data['email'])
                    print(form.cleaned_data['password'])
                else:
                    print(form.errors)
                return render(request, 'stocks/login.html')
    return render(request, 'stocks/register.html')

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