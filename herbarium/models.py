from django.contrib import admin
from .models import (
    Pessoa, Taxonomia, Colecao, RegistroColeta,
    Ocorrencia, HistoricoIdentificacao, OcorrenciaColetor,
    ComplementoEspecime, ImagemEspecime
)

# --- Configurações de Inline (Editar tabelas filhas dentro da principal) ---

class ImagemEspecimeInline(admin.TabularInline):
    model = ImagemEspecime
    extra = 1  # Quantidade de campos de imagem vazios que aparecem por padrão

class ComplementoEspecimeInline(admin.TabularInline):
    model = ComplementoEspecime
    extra = 1

class OcorrenciaColetorInline(admin.TabularInline):
    model = OcorrenciaColetor
    extra = 1

# --- Configurações Principais do Painel ---

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    # O que aparece na lista principal
    list_display = ('num_tombo', 'get_especie', 'id_colecao', 'status_submissao')
    # Filtros laterais
    list_filter = ('status_submissao', 'id_colecao')
    # Campo de busca
    search_fields = ('num_tombo', 'num_coleta')

    # Inlines para facilitar o cadastro de tudo em uma tela só
    inlines = [OcorrenciaColetorInline, ImagemEspecimeInline, ComplementoEspecimeInline]

    # Função auxiliar para mostrar a espécie na listagem
    @admin.display(description='Espécie')
    def get_especie(self, obj):
        if obj.id_identificacao_atual:
            return obj.id_identificacao_atual.id_taxon.nome_cientifico
        return "Não Identificada"

@admin.register(Taxonomia)
class TaxonomiaAdmin(admin.ModelAdmin):
    list_display = ('nome_cientifico', 'familia', 'status_taxonomico')
    search_fields = ('nome_cientifico', 'familia')
    list_filter = ('familia', 'status_taxonomico')

@admin.register(RegistroColeta)
class RegistroColetaAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'estado_provincia', 'data_coleta')
    list_filter = ('estado_provincia', 'data_coleta')

# Registros simples para as outras tabelas
admin.site.register(Pessoa)
admin.site.register(Colecao)
admin.site.register(HistoricoIdentificacao)