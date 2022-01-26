from django.shortcuts import render

# Create your views here.

def index(request):
    context = {"day":20092021}
    return render(request, 'stocks/index.html', context)

def login(request):
    return render(request, 'stocks/login.html')

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