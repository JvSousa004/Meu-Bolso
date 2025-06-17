# financas/forms.py
from django import forms
from .models import Movimentacao, Categoria, Conta
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse 
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

class MovimentacaoForm(forms.ModelForm):
    TIPO_CHOICES = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES, 
        label='Tipo de Movimentação',
        widget=forms.Select(attrs={'class': 'form-select'}) # Adicionado para Bootstrap
    )

    class Meta:
        model = Movimentacao
        fields = ['tipo', 'valor', 'data', 'categoria', 'conta', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # Adicionado para Bootstrap
            'valor': forms.NumberInput(attrs={'class': 'form-control'}), # Adicionado para Bootstrap
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), # Adicionado para Bootstrap
            'categoria': forms.Select(attrs={'class': 'form-select'}), # Adicionado para Bootstrap
            'conta': forms.Select(attrs={'class': 'form-select'}), # Adicionado para Bootstrap
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.user).order_by('nome')
            self.fields['conta'].queryset = Conta.objects.filter(usuario=self.user)
            # Para evitar que as contas do admin apareçam se o usuário não tiver uma conta
            if not self.fields['conta'].queryset.exists():
                self.fields['conta'].choices = [('', 'Crie uma conta primeiro')]
                self.fields['conta'].widget.attrs['disabled'] = 'disabled'
            if not self.fields['categoria'].queryset.exists():
                self.fields['categoria'].choices = [('', 'Crie uma categoria primeiro')]
                self.fields['categoria'].widget.attrs['disabled'] = 'disabled'


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}) # Adicionado para Bootstrap
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        categoria = super().save(commit=False)
        if self.request_user:
            categoria.usuario = self.request_user
        if commit:
            categoria.save()
        return categoria

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Adicionar classes Bootstrap aos campos do formulário de login
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

        if username and password:
            self.user_cache = None
            try:
                self.user_cache = super().clean()
            except forms.ValidationError as e:
                if 'username' in self.error_messages['invalid_login'] and 'password' in self.error_messages['invalid_login']:
                    cadastro_link = f'<a href="{reverse("financas:cadastro_usuario")}" class="alert-link">vamos criar?</a>' # Adicionado class="alert-link" para Bootstrap
                    raise forms.ValidationError(
                        _("Ops! Acho que você não tem uma conta, %s") % cadastro_link,
                        code='invalid_login',
                    )
                else:
                    raise e
        return self.user_cache 

class CustomUserCreationForm(DjangoUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Itera sobre todos os campos do formulário e adiciona a classe 'form-control'
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
