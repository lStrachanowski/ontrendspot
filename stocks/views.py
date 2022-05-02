from distutils import errors
from django.shortcuts import render
from sqlalchemy import false
from .forms import LoginForm, RegisterForm, ResetForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Stock, DataSource
from .analytics import read_stock_from_file, add_to_database, get_stock_from_db
from .charts import candle_chart

import pandas as pd
from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.http import HttpResponse  

# Create your views here.

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def index(request):
    candle_chart('pkn', 30, False)
    candle_chart('pkp', 30, False)
    context = {"day":20092021}
    return render(request, 'stocks/index.html', context)

def login_auth(request):
    if request.method == "POST" :
        if 'login_button' in request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['user']
                password = form.cleaned_data['password']
                user = authenticate(request, username=user_name, password=password)
                if user is not None:
                    if user.is_active:   
                        login(request, user)
                        response = redirect('/')
                        return response
                else:
                    f = {'message_text':'Invalid user, password or account was not activated.'}
                    return render(request, 'stocks/message.html', context=f)   
            else:
                f = {'form':form}
                return render(request, 'stocks/login.html', context=f)   

        if 'register_button' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                try:
                    user = User.objects.create_user(name, email,password)
                    user.is_active = False
                    user.save()
                    response = redirect('/confirmation')
                    return response
                except:
                    if User.objects.filter(username = name).exists():
                        f = {'message_text':'Username is already taken!'}
                        return render(request, 'stocks/message.html', context=f)  
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

        if 'error_confirm_button' in request.POST:
            return render(request, 'stocks/login.html')

    if request.method == "GET":
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
            form = RegisterForm(request.POST )
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                try:
                    user = User.objects.create_user(name, email,password)
                    user.is_active = False
                    user.save()

                    current_site = get_current_site(request)  
                    mail_subject = 'Activation link has been sent to your email id'  
                    message = render_to_string('stocks/account_activate_email.html', {  
                        'user': user,  
                        'domain': current_site.domain,  
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                        'token':account_activation_token.make_token(user),  
                    })   
                    print('test')
                    print(message)
                    # email_message = EmailMessage(  
                    #             mail_subject, message, to=[email]  
                    # )  
                    # email_message.send()  
                    response = redirect('/confirmation')
                    return response
                except Exception as e: 
                    print('Failed: '+ str(e))
                    if User.objects.filter(username = name).exists():
                        f = {'message_text':'Username is already taken!'}
                        return render(request, 'stocks/message.html', context=f)  
            else: 
                f = {'form':form}
                return render(request, 'stocks/register.html', context=f)

        if 'login_button' in request.POST :
            form = LoginForm(request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['user']
                password = form.cleaned_data['password']
                user = authenticate(request, username=user_name, password=password)
                if user is not None:
                    if user.is_active:   
                        login(request, user)
                        response = redirect('/')
                        return response
                else:
                    f = {'message_text':'Invalid user, password or account was not activated.'}
                    return render(request, 'stocks/message.html', context=f)
            else:
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

        if 'error_confirm_button' in request.POST:
            return render(request, 'stocks/register.html')
    
def confirmation(request):
    if request.method == "GET":
        return render(request, 'stocks/confirmation.html')
    if request.method == "POST":
        response = redirect('/')
        return response

@login_required(login_url='/login')      
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
    candle_chart(stockname, 90, True)
    context = {"stock":Stock.objects.get(stock_symbol=stockname.upper())}
    return render(request, 'stocks/stock.html',context )