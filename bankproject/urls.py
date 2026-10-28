from django.urls import path
from bankapp import views


urlpatterns = [
    path("", views.home, name="home"),
    path("newaccount/", views.newaccount, name="newaccount"),
    path("balance/", views.balance, name="balance"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("transfer/", views.transfer, name="transfer"),
    path("closeaccount/", views.closeaccount, name="closeaccount"),
    path('aboutus/', views.aboutus, name='aboutus'),
]