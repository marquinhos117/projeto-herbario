from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from .models import Ocorrencia, Pessoa, RegistroColeta, ImagemEspecime, Taxonomia, HistoricoIdentificacao
from .forms import CadastroUsuarioForm, RegistroColetaForm, OcorrenciaForm, IdentificacaoForm

def home(request):
    query   = request.GET.get('q', '').strip()
    familia = request.GET.get('familia', '').strip()
    taxon   = request.GET.get('taxon', '').strip()

    # Somente ocorrências aprovadas para o público
    base_qs = Ocorrencia.objects.filter(status_submissao='Aprovado').select_related(
        'id_identificacao_atual__id_taxon', 'id_registro_coleta'
    )

    # Filtros
    if query:
        base_qs = base_qs.filter(
            Q(num_tombo__icontains=query) |
            Q(id_identificacao_atual__id_taxon__nome_cientifico__icontains=query) |
            Q(id_identificacao_atual__id_taxon__familia__icontains=query) |
            Q(id_registro_coleta__municipio__icontains=query)
        )
    if familia:
        base_qs = base_qs.filter(id_identificacao_atual__id_taxon__familia__iexact=familia)
    if taxon:
        base_qs = base_qs.filter(id_identificacao_atual__id_taxon__nome_cientifico__iexact=taxon)

    # Listas para os selects dinâmicos — filtra apenas táxons de espécimes aprovados
    taxons_aprovados_ids = Ocorrencia.objects.filter(
        status_submissao='Aprovado'
    ).exclude(
        id_identificacao_atual__isnull=True
    ).values_list('id_identificacao_atual__id_taxon_id', flat=True)

    familias_disponiveis = (
        Taxonomia.objects
        .filter(id__in=taxons_aprovados_ids)
        .exclude(familia__isnull=True)
        .exclude(familia='')
        .values_list('familia', flat=True)
        .distinct()
        .order_by('familia')
    )
    taxons_disponiveis = (
        Taxonomia.objects
        .filter(id__in=taxons_aprovados_ids)
        .values_list('nome_cientifico', flat=True)
        .distinct()
        .order_by('nome_cientifico')
    )

    return render(request, 'herbarium/pages/home.html', {
        'especimes': base_qs,
        'query': query,
        'familia_sel': familia,
        'taxon_sel': taxon,
        'familias': familias_disponiveis,
        'taxons': taxons_disponiveis,
    })


def detalhe_especime(request, num_tombo):
    especime = get_object_or_404(
        Ocorrencia.objects.select_related(
            'id_identificacao_atual__id_taxon',
            'id_identificacao_atual__id_identificador',
            'id_registro_coleta',
            'id_colecao',
            'id_digitador'
        ).prefetch_related(
            'imagens',
            'historico__id_taxon',
            'historico__id_identificador',
            'ocorrenciacoletor_set__pessoa',  # tabela intermediária com e_principal
        ),
        num_tombo=num_tombo
    )
    historico = especime.historico.select_related('id_taxon', 'id_identificador').order_by('-data_identificacao')
    return render(request, 'herbarium/pages/detalhe_especime.html', {
        'especime': especime,
        'historico': historico,
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

def registrar_usuario(request):
    if request.user.is_authenticated:
        return redirect('herbarium:painel')
        
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Verifica se o username já existe
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['email']
                    
                    if User.objects.filter(username=username).exists():
                        messages.error(request, f'O nome de usuário "{username}" já está em uso.')
                        return render(request, 'herbarium/pages/cadastro.html', {'form': form})
                    
                    if User.objects.filter(email=email).exists():
                        messages.error(request, f'O email "{email}" já está cadastrado.')
                        return render(request, 'herbarium/pages/cadastro.html', {'form': form})
                    
                    # Cria o usuário do sistema do Django (Auth)
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=form.cleaned_data['password']
                    )
                    # Cria a Pessoa (perfil biológico) ligada ao usuário recém-criado
                    # Preenchemos explicitamente os campos obrigatórios
                    pessoa = Pessoa(
                        usuario=user,
                        nome_completo=form.cleaned_data['nome_completo'],
                        acronimo_coletor=form.cleaned_data['acronimo_coletor'],
                        instituicao=form.cleaned_data.get('instituicao', ''),
                        email=email,
                        nivel_acesso='ALUNO',
                    )
                    pessoa.save()

                messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
                return redirect('herbarium:login')
                
            except Exception as e:
                messages.error(request, f'Erro ao criar conta. Tente novamente.')
    else:
        form = CadastroUsuarioForm()
        
    return render(request, 'herbarium/pages/cadastro.html', {'form': form})

# View protegida! Só acessa se estiver logado.
@login_required(login_url='herbarium:login')
def painel_usuario(request):
    try:
        pessoaLogada = request.user.pessoa
        
        if pessoaLogada.nivel_acesso in ['CURADOR', 'ADMIN']:
            # Curador vê tudo que está pendente de todo mundo e os aprovados
            pendentes = Ocorrencia.objects.filter(status_submissao='Pendente')
            aprovados = Ocorrencia.objects.filter(status_submissao='Aprovado')
            contexto = {'perfil': pessoaLogada, 'pendentes': pendentes, 'aprovados': aprovados}
        else:
            # Aluno/Digitador vê apenas as próprias publicações
            minhas_ocorrencias = Ocorrencia.objects.filter(id_digitador=pessoaLogada)
            contexto = {'perfil': pessoaLogada, 'minhas_ocorrencias': minhas_ocorrencias}
            
        return render(request, 'herbarium/pages/painel.html', contexto)
    
    except Pessoa.DoesNotExist:
        messages.error(request, 'Seu usuário não possui um perfil de botânico/coletor associado. Contate o administrador.')
        return redirect('herbarium:home')

def sair(request):
    logout(request)
    return redirect('herbarium:home')

@login_required(login_url='herbarium:login')
def cadastrar_especime(request):
    if request.method == 'POST':
        coleta_form       = RegistroColetaForm(request.POST)
        ocorrencia_form   = OcorrenciaForm(request.POST)
        identificacao_form = IdentificacaoForm(request.POST)

        # Recebe os arquivos de imagem
        imagens = request.FILES.getlist('imagens_planta')

        if coleta_form.is_valid() and ocorrencia_form.is_valid() and identificacao_form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Salva os dados do local/data da coleta
                    registro_coleta = coleta_form.save()

                    # 2. Salva a Ocorrência principal (sem id_identificacao_atual ainda)
                    ocorrencia = ocorrencia_form.save(commit=False)
                    ocorrencia.id_registro_coleta = registro_coleta
                    ocorrencia.id_digitador = request.user.pessoa
                    ocorrencia.status_submissao = 'Pendente'
                    ocorrencia.save()

                    # 3. Cria o HistoricoIdentificacao ligado à ocorrência
                    identificacao = identificacao_form.save(commit=False)
                    identificacao.id_ocorrencia = ocorrencia
                    identificacao.id_identificador = request.user.pessoa
                    identificacao.save()

                    # 4. Liga a identificacao recém-criada como a identificação atual da ocorrência
                    ocorrencia.id_identificacao_atual = identificacao
                    ocorrencia.save(update_fields=['id_identificacao_atual'])

                    # 5. Associa o usuário logado como coletor
                    ocorrencia.coletores.add(request.user.pessoa)

                    # 6. Salva as imagens
                    for img in imagens:
                        ImagemEspecime.objects.create(id_ocorrencia=ocorrencia, url=img)

                messages.success(request, 'Espécime submetido com sucesso! Aguardando aprovação da curadoria.')
                return redirect('herbarium:painel')

            except Exception as e:
                messages.error(request, f'Erro ao salvar: {str(e)}')
    else:
        coleta_form        = RegistroColetaForm()
        ocorrencia_form    = OcorrenciaForm()
        identificacao_form = IdentificacaoForm()

    contexto = {
        'coleta_form': coleta_form,
        'ocorrencia_form': ocorrencia_form,
        'identificacao_form': identificacao_form,
    }
    return render(request, 'herbarium/pages/cadastrar_especime.html', contexto)
