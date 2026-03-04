from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'herbarium'

urlpatterns = [
     path('', views.home, name="home"),

]
path('curador/', views.acessar_curador, name='curador'),





