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
    
    usuario = UserSerializer(read_only=True) 
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='usuario', write_only=True 
    )

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'usuario', 'usuario_id'] 
        read_only_fields = ['id'] 
        extra_kwargs = {
            'usuario_id': {'write_only': True} 
        }

    def create(self, validated_data):
        return Categoria.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

# Serializer para Conta
class ContaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='usuario', write_only=True
    )

    class Meta:
        model = Conta
        fields = ['id', 'nome', 'saldo', 'usuario', 'usuario_id']
        read_only_fields = ['id']
        extra_kwargs = {
            'usuario_id': {'write_only': True}
        }

    def create(self, validated_data):
        return Conta.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

# Serializer para Movimentacao
class MovimentacaoSerializer(serializers.ModelSerializer):
    
    usuario = UserSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True) 
    conta = ContaSerializer(read_only=True) 
    
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
            'categoria_id', 'conta_id',      # Para escrita/criação/atualização
            # Removidas 'data_criacao' e 'data_atualizacao' daqui
        ]
        # Removidas 'data_criacao' e 'data_atualizacao' daqui também
        read_only_fields = ['id', 'usuario'] 

    def create(self, validated_data):
        return Movimentacao.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)