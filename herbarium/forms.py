from django import forms
from django.contrib.auth.models import User
from .models import Pessoa, RegistroColeta, Ocorrencia, HistoricoIdentificacao, Taxonomia

class CadastroUsuarioForm(forms.ModelForm):
    # Campos que vão para o modelo User do Django
    username = forms.CharField(max_length=150, help_text="Nome de usuário para login")
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirme a Senha")

    class Meta:
        model = Pessoa
        fields = ['nome_completo', 'acronimo_coletor', 'instituicao']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data

class RegistroColetaForm(forms.ModelForm):
    class Meta:
        model = RegistroColeta
        fields = ['data_coleta', 'pais', 'estado_provincia', 'municipio', 'localidade', 'habitat']
        widgets = {
            'data_coleta': forms.TextInput(attrs={'type': 'date', 'placeholder': 'dd/mm/aaaa', 'max': '9999-12-31'}),
        }

class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ['num_tombo', 'num_coleta', 'id_colecao']

class IdentificacaoForm(forms.ModelForm):
    """Captura os dados taxonômicos da identificação do espécime."""
    class Meta:
        model = HistoricoIdentificacao
        fields = ['id_taxon', 'data_identificacao']
        widgets = {
            'data_identificacao': forms.TextInput(attrs={'type': 'date', 'max': '9999-12-31'}),
        }
        labels = {
            'id_taxon': 'Táxon (Nome Científico)',
            'data_identificacao': 'Data da Identificação',
        }
