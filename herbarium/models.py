from django.db import models
from django.contrib.auth.models import User

# --- ATENÇÃO: NÃO ADICIONE "from .models import..." AQUI ---

# 1. PESSOA
class Pessoa(models.Model):
    NIVEIS_ACESSO = [('ALUNO', 'Aluno'), ('CURADOR', 'Curador'), ('ADMIN', 'Administrador')]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome_completo = models.CharField(max_length=150)
    acronimo_coletor = models.CharField(max_length=50)
    instituicao = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    nivel_acesso = models.CharField(max_length=20, choices=NIVEIS_ACESSO)
    status_conta = models.CharField(max_length=20, default='Ativa')
    def __str__(self): return self.nome_completo

# 2. TAXONOMIA
class Taxonomia(models.Model):
    STATUS_TAXON = [('Aceito', 'Aceito'), ('Sinônimo', 'Sinônimo')]
    nome_cientifico = models.CharField(max_length=255, unique=True)
    autor = models.CharField(max_length=100, blank=True)
    familia = models.CharField(max_length=100)
    genero = models.CharField(max_length=100)
    epiteto_especifico = models.CharField(max_length=100, blank=True)
    status_taxonomico = models.CharField(max_length=30, choices=STATUS_TAXON, default='Aceito')
    id_nome_aceito = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sinonimos')
    def __str__(self): return self.nome_cientifico

# 3. COLECAO
class Colecao(models.Model):
    acronimo = models.CharField(max_length=10, unique=True)
    nome_completo = models.CharField(max_length=150)
    id_curador = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True)
    def __str__(self): return self.nome_completo

# 4. REGISTRO_COLETA
class RegistroColeta(models.Model):
    data_coleta = models.DateField()
    pais = models.CharField(max_length=50, default="Brasil")
    estado_provincia = models.CharField(max_length=50)
    municipio = models.CharField(max_length=100)
    localidade = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    habitat = models.TextField(blank=True)
    def __str__(self): return f"{self.municipio} ({self.data_coleta})"

# 5. OCORRENCIA
class Ocorrencia(models.Model):
    STATUS_SUBMISSAO = [('Pendente', 'Pendente'), ('Aprovado', 'Aprovado')]
    num_tombo = models.CharField(max_length=50, unique=True)
    num_coleta = models.CharField(max_length=50)
    tipo_status = models.CharField(max_length=50, blank=True)
    status_submissao = models.CharField(max_length=20, choices=STATUS_SUBMISSAO, default='Pendente')
    id_digitador = models.ForeignKey(Pessoa, on_delete=models.PROTECT, related_name='digitacoes')
    id_colecao = models.ForeignKey(Colecao, on_delete=models.CASCADE)
    id_registro_coleta = models.ForeignKey(RegistroColeta, on_delete=models.CASCADE)
    id_identificacao_atual = models.ForeignKey('HistoricoIdentificacao', on_delete=models.SET_NULL, null=True, blank=True, related_name='ocorrencia_principal')
    coletores = models.ManyToManyField(Pessoa, through='OcorrenciaColetor')

# 6. HISTORICO_IDENTIFICACAO
class HistoricoIdentificacao(models.Model):
    data_identificacao = models.DateField()
    id_ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name='historico')
    id_taxon = models.ForeignKey(Taxonomia, on_delete=models.CASCADE)
    id_identificador = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True)


# 7. OCORRENCIA_COLETOR
class OcorrenciaColetor(models.Model):
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    e_principal = models.BooleanField(default=False)
    class Meta: unique_together = ('ocorrencia', 'pessoa')

# 8. COMPLEMENTO_ESPECIME
class ComplementoEspecime(models.Model):
    id_ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE)
    tipo_complemento = models.CharField(max_length=50)
    local_armazenamento = models.CharField(max_length=100)

# 9. IMAGEM_ESPECIME
class ImagemEspecime(models.Model):
    id_ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name='imagens')
    url = models.ImageField(upload_to='herbarium/fotos/')
    data_registro = models.DateField(auto_now_add=True)