from django.urls import path
from . import views

# Isso define o "sobrenome" das suas rotas
app_name = 'herbarium'

#rotas
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.acessar_login, name='login'),
    path('cadastro/', views.registrar_usuario, name='cadastro'),
    path('painel/', views.painel_usuario, name='painel'),
    path('cadastrar_especime/', views.cadastrar_especime, name='cadastrar_especime'),
    path('especime/<str:num_tombo>/', views.detalhe_especime, name='detalhe_especime'),
    path('sair/', views.sair, name='sair'),
]