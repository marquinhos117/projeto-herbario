from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Ocorrencia

def home(request):
    # Captura a busca do usuário (se houver)
    query = request.GET.get('q', '')

    if query:
        # Busca por Tombo ou Nome Científico (via Tabela Taxonomia)
        especimes = Ocorrencia.objects.filter(
            num_tombo__icontains=query
        ) | Ocorrencia.objects.filter(
            id_identificacao_atual__id_taxon__nome_cientifico__icontains=query
        )
    else:
        especimes = Ocorrencia.objects.all()

    return render(request, 'herbarium/pages/home.html', {
        'especimes': especimes,
        'query': query
    })


def acessar_login(request):
    # Regra de ouro: se a pessoa já estiver logada e tentar acessar a tela de login,
    # ela é jogada direto para o painel.
    if request.user.is_authenticated:
        return redirect('herbarium:painel') # Mude para o nome da URL do seu painel

    if request.method == 'POST':
        # Captura exatamente o que está no atributo 'name' dos seus inputs HTML
        usuario_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')

        # O Django faz a mágica da criptografia e verifica o banco de dados aqui
        user = authenticate(request, username=usuario_digitado, password=senha_digitada)

        if user is not None:
            # Se as credenciais estiverem corretas, "carimba" a sessão do usuário
            login(request, user)

            # Aqui você pode até adicionar uma lógica futura:
            # if user.nivel_acesso == 'Curador': vai pra tela X, senão tela Y

            return redirect('herbarium:painel') # Redireciona para a área restrita
        else:
            # Se a senha estiver errada, prepara uma mensagem para exibir no HTML
            messages.error(request, 'Credenciais inválidas. Verifique seu usuário e senha.')

    # Se não for POST (ou seja, a pessoa só acessou a URL), renderiza o seu HTML limpo
    return render(request, 'herbarium/pages/login.html')
