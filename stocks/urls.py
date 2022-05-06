from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('login', views.login_auth, name = "login" ),
    path('register', views.register, name = "register" ),
    path('account', views.account, name = "account"),
    path('list', views.list, name="list"),
    path('<int:date>/volume', views.daydetails, name="daydetails"),
    path('<int:date>/mean', views.daydetails, name="daydetails"),
    path('<int:date>/candles', views.daydetails, name="daydetails"),
    path('stocks/<str:stockname>', views.stock, name="stock" ),
    path('confirmation', views.confirmation, name="confirmation" ),
    path('logout', views.logout_view, name="logout"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('reset_link/<slug:uidb64>/<slug:token>/', views.reset , name="reset")
]