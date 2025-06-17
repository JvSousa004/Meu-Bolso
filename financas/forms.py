from django import forms
from .models import Movimentacao, Categoria, Conta

class MovimentacaoForm(forms.ModelForm):
    # Campo para selecionar o tipo (Receita/Despesa) com opções explícitas
    TIPO_CHOICES = [
        ('RECEITA', 'Receita'), 
        ('DESPESA', 'Despesa'),
    ]
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label='Tipo de Movimentação')

    class Meta:
        model = Movimentacao
        fields = ['tipo', 'valor', 'data', 'categoria', 'conta', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}), 
        }

    def __init__(self, *args, **kwargs):
        # O 'usuario' é passado aqui para filtrar as categorias e contas
        # que pertencem apenas a esse usuário específico.
        self.request_user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)

        if self.request_user:
            # Filtra categorias e contas para que o usuário veja apenas as suas
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.request_user).order_by('nome')
            self.fields['conta'].queryset = Conta.objects.filter(usuario=self.request_user).order_by('nome')

        # Torna a descrição opcional no formulário, mesmo que no modelo seja null=True, blank=True
        self.fields['descricao'].required = False