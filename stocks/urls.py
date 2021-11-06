from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('login', views.login, name = 'login' ),
    path('account', views.account, name = 'account'),
    path('reset', views.reset, name = 'reset'),
    path('list', views.list, name="list"),
    path('daydetails', views.daydetails, name="daydetails"),
    path('stocks/<str:stockname>', views.stock )

]