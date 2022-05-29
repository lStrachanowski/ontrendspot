from distutils import errors
from logging import error
from unicodedata import name
from django.shortcuts import render
from sqlalchemy import JSON, false
from .forms import LoginForm, RegisterForm, ResetForm, ResetEmail, FieldCheck
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
from django.shortcuts import redirect
from django.http import JsonResponse


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if 'error_confirm_button' in request.POST:
        return redirect('index')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        f = {'message_text':'Thank you for your email confirmation. Now you can login your account.'}
        return render(request, 'stocks/message.html', context=f)
    else:
        f = {'message_text':'Activation link is invalid!'}
        return render(request, 'stocks/message.html', context=f)


def reset(request, uidb64, token):
    if request.method == "GET":
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return render(request, 'stocks/change_password.html') 
        else:
            f = {'message_text':'Reset link is invalid!'}
            return render(request, 'stocks/message.html', context=f)
    if request.method == "POST":
        if 'change_password_button' in request.POST:
            form = ResetForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                uid = force_text(urlsafe_base64_decode(uidb64))
                u = User.objects.get(pk=uid)
                u.set_password(password)
                u.save()
                f = {'message_text':'Password changed'}
                return render(request, 'stocks/message.html', context=f)
            else:
                f = {'message_text':'Invalid form ??'}
                return render(request, 'stocks/message.html', context=f)  
        if 'error_confirm_button' in request.POST:
    	    return redirect('index')
    
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
 
        if 'reset_button_confirmation' in request.POST:
            form = ResetEmail(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                try:
                    user = User.objects.get(email__exact=email)
                    current_site = get_current_site(request)  
                    message = render_to_string('stocks/account_reset_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  })   
                    print(message)
                    f = {'message_text':'Check mailbox, password reset link was sent.'}
                    return render(request, 'stocks/message.html', context=f)
                except User.DoesNotExist:
                    f = {'message_text':"No account registred with this email"}
                    return render(request, 'stocks/message.html', context=f)
            else:
                f = {'message_text':form.errors.as_text}
                return render(request, 'stocks/message.html', context=f) 

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
                    # email_message = EmailMessage(  
                    #             mail_subject, message, to=[email]  
                    # )  
                    # email_message.send()  
                    print(message)
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

    
def confirmation(request):
    if request.method == "GET":
        return render(request, 'stocks/confirmation.html')
    if request.method == "POST":
        response = redirect('/')
        return response

def update_name(request):
    return JsonResponse({'user':request.user.username})

@login_required(login_url='/login')      
def account(request):
    if request.method == "POST":
        form = FieldCheck(request.POST)
        if 'user_name_save' in request.POST:
            if form.is_valid():
                new_name = form.cleaned_data['new_name']
                try:
                    User.objects.get(username = new_name)
                    f = {'message_text':'User exists, choose other name.'}
                    return render(request, 'stocks/message.html', context=f)  
                except User.DoesNotExist:
                    new_user = User.objects.get(username = request.user.username)
                    new_user.username = new_name
                    new_user.save()
            else:
                f = {'message_text':'Invalid username'}
                return render(request, 'stocks/message.html', context=f)   
        if 'user_email_save' in request.POST:
            print('save email')
    return render(request, 'stocks/account.html')

def edit(request):
    return render(request, 'stocks/edit.html')

def list(request):
    return render(request, 'stocks/list.html')

def daydetails(request, date):
    return render(request, 'stocks/daydetails.html')

def stock(request, stockname):
    candle_chart(stockname, 90, True)
    context = {"stock":Stock.objects.get(stock_symbol=stockname.upper())}
    return render(request, 'stocks/stock.html',context )


def csrf_failure(request, reason=""):
    if 'error_confirm_button' in request.POST:
        return render(request, 'stocks/index.html')
    f = {'message_text':'Something went wrong'}
    return render(request, 'stocks/message.html', context=f) 

def page_not_found(request, exception=None):
    return render(request, 'stocks/404.html', status=404)