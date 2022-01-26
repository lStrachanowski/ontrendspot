from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('login', views.login, name = "login" ),
    path('account', views.account, name = "account"),
    path('reset', views.reset, name = "reset"),
    path('list', views.list, name="list"),
    path('<int:date>/volume', views.daydetails, name="daydetails"),
    path('<int:date>/mean', views.daydetails, name="daydetails"),
    path('<int:date>/candles', views.daydetails, name="daydetails"),
    path('stocks/<str:stockname>', views.stock, name="stock" )
]