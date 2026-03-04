from django.contrib import admin
from .models import (
    Pessoa, Taxonomia, Colecao, RegistroColeta,
    Ocorrencia, HistoricoIdentificacao, OcorrenciaColetor,
    ComplementoEspecime, ImagemEspecime
)

# Inlines para facilitar o cadastro de imagens e coletores dentro da Ocorrência
class ImagemEspecimeInline(admin.TabularInline):
    model = ImagemEspecime
    extra = 1

class OcorrenciaColetorInline(admin.TabularInline):
    model = OcorrenciaColetor
    extra = 1

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('num_tombo', 'status_submissao', 'id_colecao')
    search_fields = ('num_tombo', 'num_coleta')
    inlines = [OcorrenciaColetorInline, ImagemEspecimeInline]

@admin.register(Taxonomia)
class TaxonomiaAdmin(admin.ModelAdmin):
    list_display = ('nome_cientifico', 'familia', 'genero')
    search_fields = ('nome_cientifico', 'familia')

@admin.register(RegistroColeta)
class RegistroColetaAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'estado_provincia', 'data_coleta')

# Registros simples para as demais tabelas
admin.site.register(Pessoa)
admin.site.register(Colecao)
admin.site.register(HistoricoIdentificacao)
admin.site.register(OcorrenciaColetor)
admin.site.register(ComplementoEspecime)
admin.site.register(ImagemEspecime)