# Meu-Bolso/financas/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Categoria, Conta, Movimentacao

# Classe de teste para autenticação e permissões
class AuthTests(APITestCase):

    def setUp(self):
        # Cria um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True, is_superuser=True)
        
        # Cria um segundo usuário para testar acesso a dados de outros
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')

        # URLs base para os ViewSets
        self.movimentacao_list_url = reverse('movimentacao-list')
        self.categoria_list_url = reverse('categoria-list')
        self.conta_list_url = reverse('conta-list')

        # Cria uma categoria, conta e movimentacao para o user principal
        self.categoria = Categoria.objects.create(nome='Alimentação', usuario=self.user)
        self.conta = Conta.objects.create(nome='Conta Principal', saldo=1000.00, usuario=self.user)
        self.movimentacao = Movimentacao.objects.create(
            tipo='DESPESA',
            valor=50.00,
            data='2025-06-20',
            descricao='Jantar',
            usuario=self.user,
            categoria=self.categoria,
            conta=self.conta
        )

        # Cria uma categoria, conta e movimentacao para o outro user
        self.other_categoria = Categoria.objects.create(nome='Transporte', usuario=self.other_user)
        self.other_conta = Conta.objects.create(nome='Carteira', saldo=200.00, usuario=self.other_user)
        self.other_movimentacao = Movimentacao.objects.create(
            tipo='RECEITA',
            valor=100.00,
            data='2025-06-19',
            descricao='Venda',
            usuario=self.other_user,
            categoria=self.other_categoria,
            conta=self.other_conta
        )
        
        # URL de detalhe para testar permissões de objeto
        self.movimentacao_detail_url = reverse('movimentacao-detail', kwargs={'pk': self.movimentacao.id})
        self.other_movimentacao_detail_url = reverse('movimentacao-detail', kwargs={'pk': self.other_movimentacao.id})

    # --- Testes de Autenticação e Permissões ---

    def test_acesso_nao_autenticado_movimentacoes(self):
        """
        Garante que usuários não autenticados não podem listar movimentações.
        """
        response = self.client.get(self.movimentacao_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_acesso_autenticado_movimentacoes(self):
        """
        Garante que usuários autenticados podem listar suas próprias movimentações.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.movimentacao_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica se o usuário só vê suas próprias movimentações
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.movimentacao.id)


    def test_usuario_nao_pode_ver_movimentacao_de_outro_usuario(self):
        """
        Garante que um usuário não pode acessar o detalhe da movimentação de outro.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.other_movimentacao_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Ou 403 Forbidden dependendo da sua query


    def test_usuario_nao_pode_atualizar_movimentacao_de_outro_usuario(self):
        """
        Garante que um usuário não pode atualizar a movimentação de outro.
        """
        self.client.force_authenticate(user=self.user)
        data = {'valor': 999.00} # Dados para tentar atualizar
        response = self.client.patch(self.other_movimentacao_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Ou 403 Forbidden

    def test_usuario_nao_pode_deletar_movimentacao_de_outro_usuario(self):
        """
        Garante que um usuário não pode deletar a movimentação de outro.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.other_movimentacao_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Ou 403 Forbidden


# Classe de teste para o CRUD de Movimentações
class MovimentacaoTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user) # Autentica o cliente para todos os testes desta classe

        self.categoria = Categoria.objects.create(nome='Compras', usuario=self.user)
        self.conta = Conta.objects.create(nome='Carteira', saldo=500.00, usuario=self.user)

        self.list_url = reverse('movimentacao-list')

    def test_criar_movimentacao(self):
        """
        Garante que podemos criar uma nova movimentação.
        """
        data = {
            'tipo': 'DESPESA',
            'valor': 150.00,
            'data': '2025-06-22',
            'descricao': 'Supermercado',
            'usuario_id': self.user.id,
            'categoria_id': self.categoria.id,
            'conta_id': self.conta.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movimentacao.objects.count(), 1)
        self.assertEqual(Movimentacao.objects.get().descricao, 'Supermercado')
        self.assertEqual(response.data['usuario']['id'], self.user.id) # Verifica o usuário atribuído

    def test_criar_movimentacao_dados_invalidos(self):
        """
        Garante que não podemos criar uma movimentação com dados inválidos.
        """
        data = {
            'tipo': 'TIPO_INVALIDO', # Tipo inválido
            'valor': 'ABC',         # Valor inválido
            'data': '2025-06-22',
            'descricao': 'Teste',
            'usuario_id': self.user.id,
            'categoria_id': self.categoria.id,
            'conta_id': self.conta.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tipo', response.data) # Verifica se o erro do campo 'tipo' está na resposta
        self.assertIn('valor', response.data) # Verifica se o erro do campo 'valor' está na resposta
        self.assertEqual(Movimentacao.objects.count(), 0) # Nenhuma movimentação deve ter sido criada

    def test_listar_movimentacoes(self):
        """
        Garante que podemos listar todas as movimentações.
        """
        Movimentacao.objects.create(
            tipo='RECEITA', valor=200.00, data='2025-06-21', descricao='Salário',
            usuario=self.user, categoria=self.categoria, conta=self.conta
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_detalhe_movimentacao(self):
        """
        Garante que podemos buscar uma movimentação específica.
        """
        movimentacao = Movimentacao.objects.create(
            tipo='DESPESA', valor=75.00, data='2025-06-23', descricao='Gasolina',
            usuario=self.user, categoria=self.categoria, conta=self.conta
        )
        detail_url = reverse('movimentacao-detail', kwargs={'pk': movimentacao.id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['descricao'], 'Gasolina')

    def test_atualizar_movimentacao(self):
        """
        Garante que podemos atualizar uma movimentação existente.
        """
        movimentacao = Movimentacao.objects.create(
            tipo='RECEITA', valor=100.00, data='2025-06-24', descricao='Freelance',
            usuario=self.user, categoria=self.categoria, conta=self.conta
        )
        detail_url = reverse('movimentacao-detail', kwargs={'pk': movimentacao.id})
        updated_data = {'valor': 120.00, 'descricao': 'Freelance - Atualizado'}
        response = self.client.patch(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movimentacao.refresh_from_db()
        self.assertEqual(movimentacao.valor, 120.00)
        self.assertEqual(movimentacao.descricao, 'Freelance - Atualizado')

    def test_deletar_movimentacao(self):
        """
        Garante que podemos deletar uma movimentação.
        """
        movimentacao = Movimentacao.objects.create(
            tipo='DESPESA', valor=25.00, data='2025-06-25', descricao='Café',
            usuario=self.user, categoria=self.categoria, conta=self.conta
        )
        detail_url = reverse('movimentacao-detail', kwargs={'pk': movimentacao.id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movimentacao.objects.count(), 0)

# TODO: Repita as classes de teste para CategoriaTests e ContaTests, seguindo o padrão acima.
# Lembre-se de adaptar os dados e as URLs.