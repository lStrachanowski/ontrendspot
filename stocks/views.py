from distutils import errors
import email
from logging import error
import re
from unicodedata import name
from urllib import request
from django.shortcuts import render
from sqlalchemy import JSON, false
from .forms import LoginForm, RegisterForm, ResetForm, ResetEmail, FieldCheck, EmailCheck, ChangePassword
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Stock, DataSource
from .analytics import read_stock_from_file, add_to_database, get_stock_from_db, stocks_files_paths, update_database, add_stock_informations, \
    get_stock_mean_volume_value, percent_volume_change, get_stocks_mean_volumes, analyze_percent_changes, add_missing_stock_data, read_daylist, add_daylist_to_db, get_key_dates,\
    sma_calculation, sma_signals, get_tickers, get_sma_results_from_db, sma_template_data, sma_elements, get_unique_dates, get_crossing_dates, candle_pattern, rename_candles_to_db,\
    add_candle_data_to_db, template_mean_volume
from .charts import candle_chart, histogram, mean_volume_chart, rolling_mean_charts, rsi_chart, bollinger_bands_chart, mean_volume_chart, daily_returns_chart, stock_changes
import pandas as pd
from datetime import datetime, timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
import json
import plotly
from django.utils import timezone
from django.http import HttpResponse
import pandas as pd
from .candlesNames import candle_name_table


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if 'error_confirm_button' in request.POST:
        return redirect('index')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        f = {'message_text': 'Thank you for your email confirmation. Now you can login your account.'}
        return render(request, 'stocks/message.html', context=f)
    else:
        f = {'message_text': 'Activation link is invalid!'}
        return render(request, 'stocks/message.html', context=f)


def reset(request, uidb64, token):
    if request.method == "GET":
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return render(request, 'stocks/change_password.html')
        else:
            f = {'message_text': 'Reset link is invalid!'}
            return render(request, 'stocks/message.html', context=f)
    if request.method == "POST":
        if 'change_password_button' in request.POST:
            form = ResetForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                uid = force_str(urlsafe_base64_decode(uidb64))
                u = User.objects.get(pk=uid)
                u.set_password(password)
                u.save()
                f = {'message_text': 'Password changed'}
                return render(request, 'stocks/message.html', context=f)
            else:
                f = {'message_text': 'Invalid form ??'}
                return render(request, 'stocks/message.html', context=f)
        if 'error_confirm_button' in request.POST:
            return redirect('index')


def index(request):
    # SMA data 
    dates = sma_elements(get_key_dates(3))
    sma_data_15_45 = sma_template_data(dates, 'sma_15', 'sma_45')
    sma_data_50_200 = sma_template_data(dates, 'sma_50', 'sma_200')
    volume_days = []
    candle_days = []
    # Candle data
    cande_data = read_daylist('C')
    candle_keys = cande_data.groups.keys()
    last_key_candle = [key for key in candle_keys][-1]
    for candle_date, candle_value in cande_data:
        if candle_date == last_key_candle:
            candle_value = candle_value.drop('option', axis=1)
            candle_days.append({"day": str(last_key_candle), "stock": candle_value['stock_symbol'].tolist(
            ), "candle": candle_value['candles'].tolist()})
    tickers = [candle.split("_") for candle in candle_days[0]['candle']]
    values = [value for value in candle_days[0]['stock']]
    candle_data = zip(values, tickers)

    candle_data_up_for_template = []
    candle_data_down_for_template = []
    for value in candle_data:
        if value[1][1] == "UP":
            if value[1][0] in candle_name_table:
                value[1][0] = candle_name_table[value[1][0]]
            candle_data_up_for_template.append(
                {"day": candle_days[0]['day'], "stock_data": value})
        else:
            if value[1][0] in candle_name_table:
                value[1][0] = candle_name_table[value[1][0]]
                candle_data_down_for_template.append(
                    {"day": candle_days[0]['day'], "stock_data": value})
    # Volume data
    volumen_data = read_daylist('V')
    volumen_keys = volumen_data.groups.keys()
    last_key_volumen = [key for key in volumen_keys][-1]
    for value in volumen_data:
        if value[0] == last_key_volumen:
            volume_days.append(
                {"day": str(last_key_volumen), "stock": value[1][0:2]['stock_symbol'].tolist()})

    for item in volume_days[0]["stock"]:
        candle_chart(item, 30, False, 'image')
    context = {"day":  volume_days[0]["day"],
               "tickers": volume_days[0]["stock"],
               "smadata_15_45": sma_data_15_45,
               "smadata_50_200": sma_data_50_200,
               "candle_data_up": candle_data_up_for_template,
               "candle_data_down": candle_data_down_for_template}

    if request.user.is_authenticated:
        context = {"day":  volume_days[0]["day"],
                   "tickers": volume_days[0]["stock"],
                   "smadata_15_45": sma_data_15_45,
                   "smadata_50_200": sma_data_50_200,
                   "candle_data_up": candle_data_up_for_template,
                   "candle_data_down": candle_data_down_for_template}

    return render(request, 'stocks/index.html', context)


def login_auth(request):
    if request.method == "POST":
        if 'login_button' in request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['user']
                password = form.cleaned_data['password']
                user = authenticate(
                    request, username=user_name, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        response = redirect('/')
                        return response
                else:
                    f = {
                        'message_text': 'Invalid user, password or account was not activated.'}
                    return render(request, 'stocks/message.html', context=f)
            else:
                f = {'form': form}
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
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user), })
                    print(message)
                    f = {'message_text': 'Check mailbox, password reset link was sent.'}
                    return render(request, 'stocks/message.html', context=f)
                except User.DoesNotExist:
                    f = {'message_text': "No account registred with this email"}
                    return render(request, 'stocks/message.html', context=f)
            else:
                f = {'message_text': form.errors.as_text}
                return render(request, 'stocks/message.html', context=f)

        if 'error_confirm_button' in request.POST:
            return render(request, 'stocks/login.html')

    if request.method == "GET":
        return render(request, 'stocks/login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    response = redirect('/')
    return response


def register(request):
    if request.method == "GET":
        return render(request, 'stocks/register.html')
    if request.method == "POST":
        if 'register_button' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                if User.objects.filter(email__exact=email).exists():
                    f = {'message_text': 'Email address is already taken!'}
                    return render(request, 'stocks/message.html', context=f)
                else:
                    try:
                        user = User.objects.create_user(name, email, password)
                        user.is_active = False
                        user.save()
                        current_site = get_current_site(request)
                        mail_subject = 'Activation link has been sent to your email id'
                        message = render_to_string('stocks/account_activate_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        # email_message = EmailMessage(
                        #             mail_subject, message, to=[email]
                        # )
                        # email_message.send()
                        print(message)
                        response = redirect('/confirmation')
                        return response
                    except Exception as e:
                        if User.objects.filter(username=name).exists():
                            f = {'message_text': 'Username is already taken!'}
                            return render(request, 'stocks/message.html', context=f)
            else:
                f = {'form': form}
                return render(request, 'stocks/register.html', context=f)

        if 'error_confirm_button' in request.POST:
            return render(request, 'stocks/register.html')


def confirmation(request):
    if request.method == "GET":
        return render(request, 'stocks/confirmation.html')
    if request.method == "POST":
        response = redirect('/')
        return response


def update_name(request):
    return JsonResponse({'user': request.user.username, 'email': request.user.email})


@login_required(login_url='/login')
def account(request):
    context = {"time": "test"}
    if request.method == "POST":
        if 'user_name_save' in request.POST:
            form = FieldCheck(request.POST)
            if form.is_valid():
                new_name = form.cleaned_data['new_name']
                try:
                    User.objects.get(username=new_name)
                    f = {'message_text': 'User exists, choose other name.'}
                    return render(request, 'stocks/message.html', context=f)
                except User.DoesNotExist:
                    new_user = User.objects.get(username=request.user.username)
                    new_user.username = new_name
                    new_user.save()
            else:
                f = {'message_text': 'Invalid username'}
                return render(request, 'stocks/message.html', context=f)
        if 'user_email_save' in request.POST:
            form = EmailCheck(request.POST)
            if form.is_valid():
                new_email = form.cleaned_data['new_email']
                try:
                    check_email = User.objects.filter(email=new_email)
                    if check_email[0]:
                        f = {
                            'message_text': 'Email is already used , please enter new email.'}
                        return render(request, 'stocks/message.html', context=f)
                except:
                    current_email = User.objects.get(email=request.user.email)
                    current_email.email = new_email
                    current_email.save()
            else:
                f = {'message_text': 'Invalid email'}
                return render(request, 'stocks/message.html', context=f)
        if 'saveButton' in request.POST:
            form = ChangePassword(request.POST)
            if form.is_valid():
                oldPass = form.cleaned_data['oldPass']
                newPass = form.cleaned_data['newPass']
                confirmNewPass = form.cleaned_data['confirmNewPass']
                user = authenticate(
                    username=request.user.username, password=oldPass)
                if user is not None:
                    user.set_password(confirmNewPass)
                    user.save()
                    f = {'message_text': 'Password was changed'}
                    return render(request, 'stocks/message.html', context=f)
                else:
                    f = {'message_text': 'Please enter correct current password.'}
                    return render(request, 'stocks/message.html', context=f)
            else:
                f = {'form': form}
                return render(request, 'stocks/account.html', context=f)
    return render(request, 'stocks/account.html', context)


def edit(request):
    return render(request, 'stocks/edit.html')


def list(request):
    volumen_data = read_daylist('V')
    crossing_data = read_daylist('M')
    candle_data = read_daylist('C')

    candle_days = [str(v[0]) for v in candle_data]

    sma_15_45_dates = get_crossing_dates(crossing_data)[0]
    sma_50_200_dates = get_crossing_dates(crossing_data)[1]

    volumen_dates = [str(key) for key in volumen_data.groups.keys()]
    volumen_dates.reverse()


    context = {"volumen_dates": volumen_dates,
               "sma_15_45": get_unique_dates(sma_15_45_dates), "sma_50_200": get_unique_dates(sma_50_200_dates), "candle_dates":get_unique_dates(candle_days)}
    return render(request, 'stocks/list.html', context)


def show_more_list_values(request, link):
    if link == "V":
        volumen_data = read_daylist('V')
        dates = [str(key) for key in volumen_data.groups.keys()]
        dates.reverse()

    if link == "sma_15_45_list":
        crossing_data = read_daylist('M')
        sma_dates = get_crossing_dates(crossing_data)[0]
        dates = get_unique_dates(sma_dates)

    if link == "sma_50_200_list":
        crossing_data = read_daylist('M')
        sma_dates = get_crossing_dates(crossing_data)[1]
        dates = get_unique_dates(sma_dates)

    if link == "CandlePattern":
        candle_data = read_daylist('C')
        candle_days = [str(v[0]) for v in candle_data]
        dates = get_unique_dates(candle_days)
        # For development only 
        dates = dates + ['2023-07-23', '2023-01-07', '2023-01-03']
    return JsonResponse({'values': dates})


def daydetails(request, date):
    stock_list = []
    graph = []
    daily_percent_change = []
    stock_close = []
    mean_values_list = []
    data = read_daylist('V')
    for value in data:
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
        if value[0] == date_object:
            stock_list = value[1]['stock_symbol'].tolist()
    for ticker in stock_list:
        mean_data = template_mean_volume(ticker, date , [1,5,30])
        mean_values_list.append(mean_data)
        daily_percent_change.append(stock_changes(
            ticker, 2, 1).dropna().iloc[0].round(3))
        stock_close.append(get_stock_from_db(ticker, 1)['stock_close'].iloc[0])
        graph.append(candle_chart(ticker, 90, True, 'fig'))
    stock_data = zip(stock_list, daily_percent_change, stock_close, mean_values_list)
    context = {"graphJSON": json.dumps(
        graph, cls=plotly.utils.PlotlyJSONEncoder), "charts": stock_data, "chartData": stock_list, "day": date, "stocksQuantity":len(stock_list)}
    return render(request, 'stocks/daydetails.html', context)

def mean_view(request, date, interval1, interval2):
    daily_percent_change = []
    stock_close = []
    graph = []
    stock_list = []
    data = get_sma_results_from_db()
    date_object = datetime.strptime(date, '%Y-%m-%d').date()
    result_data = data[data['Date'] == date_object]
    for value in result_data.iterrows():
        if int(value[1]['Crossing'].split(" ")[0].split("_")[1]) == interval1:
            ticker = value[1]['Ticker']
            daily_percent_change.append(stock_changes(ticker, 2, 1).dropna().iloc[0].round(3))
            stock_close.append(get_stock_from_db(ticker, 1)['stock_close'].iloc[0])
            if interval2 > 50:
                graph.append(rolling_mean_charts(ticker, 365, [interval1, interval2])) 
            else:
                graph.append(rolling_mean_charts(ticker, 120, [interval1, interval2]))
            stock_list.append(ticker)
    stock_data = zip(stock_list, daily_percent_change, stock_close)
    context = {"graphJSON": graph, "stockData": stock_data, "stocksTickers": stock_list, "day": date, "stocksQuantity":len(stock_list)}
    return render(request, 'stocks/meandetails.html', context )


def candles_view(request, date):
    candle_data = read_daylist('C')
    candle_days = []
    candle_data_up_for_template = []
    candle_data_down_for_template = []
    candle_keys = candle_data.groups.keys()
    last_key_candle = [key for key in candle_keys][-1]
    for candle_date, candle_value in candle_data:
        if candle_date == last_key_candle:
            candle_value = candle_value.drop('option', axis=1)
            candle_days.append({"day": str(last_key_candle), "stock": candle_value['stock_symbol'].tolist(
            ), "candle": candle_value['candles'].tolist()})
    tickers = [candle.split("_") for candle in candle_days[0]['candle']]
    values = [value for value in candle_days[0]['stock']]
    candle_data = zip(values, tickers)

    for value in candle_data:
        if value[1][1] == "UP":
            if value[1][0] in candle_name_table:
                value[1][0] = candle_name_table[value[1][0]]
            candle_data_up_for_template.append(
                {"day": candle_days[0]['day'], "stock_data": value})
        else:
            if value[1][0] in candle_name_table:
                value[1][0] = candle_name_table[value[1][0]]
                candle_data_down_for_template.append(
                    {"day": candle_days[0]['day'], "stock_data": value})

    context = {"day": date,
               "candle_data_up": candle_data_up_for_template,
               "candle_data_down": candle_data_down_for_template}
    return render(request, 'stocks/candlesdetails.html', context )

def stock(request, stockname):
    daily_percent_change = stock_changes(
        stockname, 2, 1).dropna().iloc[0].round(3)
    stock_close = get_stock_from_db(stockname, 1)['stock_close'].iloc[0]
    graphJSON = candle_chart(stockname, 90, True, 'json')
    histogramJSON = histogram(stockname, 90)
    rollingMeanJSON = rolling_mean_charts(stockname, 180, [15, 30, 45])
    rsiJSON = rsi_chart(stockname, 180)
    bbandsJSON = bollinger_bands_chart(stockname, 180)
    mean_volumeJSON = mean_volume_chart(stockname, 365)
    daily_returnsJSON = daily_returns_chart(stockname, 90)
    context = {"graphJSON": graphJSON,
               "histChart": histogramJSON,
               "rollingMean": rollingMeanJSON,
               "rsi": rsiJSON,
               "bollinger": bbandsJSON,
               "mean_volume": mean_volumeJSON,
               "daily_returns": daily_returnsJSON,
               "stock": Stock.objects.get(stock_symbol=stockname.upper()),
               "daily_change": daily_percent_change,
               "stock_close": stock_close}
    return render(request, 'stocks/stock.html', context)


def csrf_failure(request, reason=""):
    if 'error_confirm_button' in request.POST:
        return render(request, 'stocks/index.html')
    f = {'message_text': 'Something went wrong'}
    return render(request, 'stocks/message.html', context=f)


def page_not_found(request, exception=None):
    return render(request, 'stocks/404.html', status=404)

