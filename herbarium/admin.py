from django.contrib import admin
# IMPORTANTE: Os nomes abaixo devem ser EXATAMENTE os que estão no seu models.py
from .models import (
    Pessoa, Taxonomia, Colecao, RegistroColeta,
    Ocorrencia, HistoricoIdentificacao, OcorrenciaColetor,
    ComplementoEspecime, ImagemEspecime
)

# Inlines para facilitar o cadastro (Permite adicionar fotos e coletores na mesma tela da Ocorrência)
class ImagemEspecimeInline(admin.TabularInline):
    model = ImagemEspecime
    extra = 1

class OcorrenciaColetorInline(admin.TabularInline):
    model = OcorrenciaColetor
    extra = 1

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    # Ajustado para os nomes dos campos da Tabela 5
    list_display = ('num_tombo', 'num_coleta', 'status_submissao', 'id_colecao')
    search_fields = ('num_tombo', 'num_coleta')
    inlines = [OcorrenciaColetorInline, ImagemEspecimeInline]

@admin.register(Taxonomia)
class TaxonomiaAdmin(admin.ModelAdmin):
    # Ajustado para os nomes dos campos da Tabela 2
    list_display = ('nome_cientifico', 'familia', 'genero', 'status_taxonomico')
    search_fields = ('nome_cientifico', 'familia')
    list_filter = ('familia', 'status_taxonomico')

@admin.register(RegistroColeta)
class RegistroColetaAdmin(admin.ModelAdmin):
    # Ajustado para os nomes dos campos da Tabela 4
    list_display = ('municipio', 'estado_provincia', 'data_coleta')
    list_filter = ('estado_provincia',)

# Registros simples para as tabelas de apoio
admin.site.register(Pessoa)
admin.site.register(Colecao)
admin.site.register(HistoricoIdentificacao)
admin.site.register(OcorrenciaColetor)
admin.site.register(ComplementoEspecime)
admin.site.register(ImagemEspecime)