from django.urls import path
from poke import views

urlpatterns = [
    path('', views.index),
    path('main/', views.main),
    path('pokes/', views.pokes),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
]