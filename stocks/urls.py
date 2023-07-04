from unicodedata import name
from django.urls import path
from .import views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    path('', views.index , name="index"),
    path('login', views.login_auth, name = "login" ),
    path('register', views.register, name = "register" ),
    path('account', views.account, name = "account"),
    path('list', views.list, name="list"),
    path('<str:date>/volume', views.daydetails, name="daydetails"),
    path('<str:date>/mean/<int:interval1>/<int:interval2>', views.mean_view, name="mean_details"),
    path('<str:date>/candles', views.candles_view, name="candle_details"),
    path('stocks/<str:stockname>', views.stock, name="stock" ),
    path('confirmation', views.confirmation, name="confirmation" ),
    path('logout', views.logout_view, name="logout"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('reset_link/<slug:uidb64>/<slug:token>/', views.reset , name="reset"),
    path('update', views.update_name, name="update"),
    path('morevalues/<str:link>', views.show_more_list_values, name="morevalues" ),
    path("favicon.ico",RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")))
]

