from django.shortcuts import render
from .models import Ocorrencia # Importando o modelo em português conforme seu arquivo

def index(request):
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

    return render(request, 'herbarium/index.html', {
        'especimes': especimes,
        'query': query
    })


def acessar_curador(request):
    return render(request, 'pages/acessar_curador.html')