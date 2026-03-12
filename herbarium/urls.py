from django.urls import path
from . import views

# Isso define o "sobrenome" das suas rotas
app_name = 'herbarium'

#rotas
urlpatterns = [

    path('', views.home, name="home"),
    path('login/', views.acessar_login, name='login'),
]