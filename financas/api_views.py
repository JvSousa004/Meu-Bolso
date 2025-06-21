from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Movimentacao, Categoria, Conta
from .serializers import MovimentacaoSerializer, CategoriaSerializer, ContaSerializer
from django.contrib.auth.models import User 


# ViewSet para Movimentações
class MovimentacaoViewSet(viewsets.ModelViewSet):
  
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna apenas as movimentações pertencentes ao usuário logado,
        ordenadas por data e ID (para garantir ordem estável).
        """
        return Movimentacao.objects.filter(usuario=self.request.user).order_by('-data', '-id')

    def perform_create(self, serializer):
        """
        Ao criar uma nova movimentação, associa o usuário logado a ela.
        A lógica de atualização de saldo já deve estar no método save()
        do modelo Movimentacao ou em um signal.
        """
        
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        """
        Ao atualizar uma movimentação, associa o usuário logado a ela.
        """
      
        serializer.save(usuario=self.request.user)


# ViewSet para Categorias
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna apenas as categorias pertencentes ao usuário logado.
        """
        return Categoria.objects.filter(usuario=self.request.user).order_by('nome')

    def perform_create(self, serializer):
        """
        Ao criar uma nova categoria, associa o usuário logado a ela.
        Adiciona validação para evitar nomes de categorias duplicados por usuário.
        """
        nome_categoria = serializer.validated_data.get('nome')
        if Categoria.objects.filter(usuario=self.request.user, nome__iexact=nome_categoria).exists():
            raise status.HTTP_400_BAD_REQUEST("Já existe uma categoria com este nome para este usuário.")
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        """
        Ao atualizar uma categoria, associa o usuário logado a ela.
        Adiciona validação para evitar nomes de categorias duplicados por usuário.
        """
        nome_categoria = serializer.validated_data.get('nome')
        
        if Categoria.objects.filter(usuario=self.request.user, nome__iexact=nome_categoria).exclude(pk=serializer.instance.pk).exists():
            raise status.HTTP_400_BAD_REQUEST("Já existe outra categoria com este nome para este usuário.")
        serializer.save(usuario=self.request.user)


# ViewSet para Contas
class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna apenas as contas pertencentes ao usuário logado.
        """
        return Conta.objects.filter(usuario=self.request.user).order_by('nome')

    def perform_create(self, serializer):
        """
        Ao criar uma nova conta, associa o usuário logado a ela.
        Adiciona validação para evitar nomes de contas duplicados por usuário.
        """
        nome_conta = serializer.validated_data.get('nome')
        if Conta.objects.filter(usuario=self.request.user, nome__iexact=nome_conta).exists():
            raise status.HTTP_400_BAD_REQUEST("Já existe uma conta com este nome para este usuário.")
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        """
        Ao atualizar uma conta, associa o usuário logado a ela.
        Adiciona validação para evitar nomes de contas duplicados por usuário.
        """
        nome_conta = serializer.validated_data.get('nome')
        
        if Conta.objects.filter(usuario=self.request.user, nome__iexact=nome_conta).exclude(pk=serializer.instance.pk).exists():
            raise status.HTTP_400_BAD_REQUEST("Já existe outra conta com este nome para este usuário.")
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        """
        Endpoint customizado para retornar o saldo total e as últimas movimentações do usuário.
        Acessível em /api/contas/dashboard/
        """
        user = request.user
        
        try:
            conta_principal = Conta.objects.get(usuario=user)
        except Conta.DoesNotExist:
           
            conta_principal = Conta.objects.create(usuario=user, nome='Conta Principal', saldo=0.00)

       
        ultimas_movimentacoes_queryset = Movimentacao.objects.filter(usuario=user).order_by('-data', '-id')[:5]
       
        ultimas_movimentacoes_serializer = MovimentacaoSerializer(ultimas_movimentacoes_queryset, many=True, context={'request': request})

        return Response({
            "saldo_total": float(conta_principal.saldo), 
            "ultimas_movimentacoes": ultimas_movimentacoes_serializer.data
        }, status=status.HTTP_200_OK)