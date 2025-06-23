from rest_framework import serializers
from .models import Movimentacao, Categoria, Conta
from django.contrib.auth.models import User

# Serializer para o modelo User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['username', 'email', 'first_name', 'last_name']

class CategoriaSerializer(serializers.ModelSerializer):
    # 'usuario' é apenas para leitura; será preenchido pelo ViewSet
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Categoria
        # Removemos 'usuario_id' daqui, pois ele será definido pelo ViewSet.
        # 'usuario' agora está explicitamente em read_only_fields.
        fields = ['id', 'nome', 'usuario']
        read_only_fields = ['id', 'usuario'] # <--- Adicionado 'usuario' aqui

    # Os métodos create e update geralmente não precisam ser sobrescritos
    # em serializers simples quando o ViewSet gerencia o 'owner'.
    # Deixando-os como padrão ou removendo-os (se você não tiver lógica extra aqui)
    # é comum. Por enquanto, não os modificaremos se não causarem problemas.

# Serializer para Conta
class ContaSerializer(serializers.ModelSerializer):
    # 'usuario' é apenas para leitura; será preenchido pelo ViewSet
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Conta
        # Removemos 'usuario_id' daqui, pois ele será definido pelo ViewSet.
        # 'usuario' agora está explicitamente em read_only_fields.
        fields = ['id', 'nome', 'saldo', 'usuario']
        read_only_fields = ['id', 'usuario'] # <--- Adicionado 'usuario' aqui

    # Os métodos create e update geralmente não precisam ser sobrescritos
    # em serializers simples quando o ViewSet gerencia o 'owner'.

# Serializer para Movimentacao
class MovimentacaoSerializer(serializers.ModelSerializer):
    # 'usuario' é apenas para leitura; será preenchido pelo ViewSet
    usuario = UserSerializer(read_only=True)
    # 'categoria' e 'conta' são para leitura (aninhados)
    categoria = CategoriaSerializer(read_only=True)
    conta = ContaSerializer(read_only=True)

    # Estes campos são para escrita: o usuário *escolhe* a categoria e a conta
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True, required=False
    )
    conta_id = serializers.PrimaryKeyRelatedField(
        queryset=Conta.objects.all(), source='conta', write_only=True
    )

    class Meta:
        model = Movimentacao
        fields = [
            'id', 'tipo', 'valor', 'data', 'descricao',
            'usuario', 'categoria', 'conta', # Para leitura
            'categoria_id', 'conta_id',      # Para escrita (IDs de categoria/conta escolhidos pelo usuário)
        ]
        # 'usuario' é adicionado a read_only_fields, como nos outros.
        read_only_fields = ['id', 'usuario'] # <--- Adicionado 'usuario' aqui

   