from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'stocks/index.html')

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

def daydetails(request):
    return render(request, 'stocks/daydetails.html')

def stock(request, stockname):
    context = {"name":stockname}
    return render(request, 'stocks/stock.html',context )