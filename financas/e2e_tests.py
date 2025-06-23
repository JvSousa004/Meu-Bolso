from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse


from financas.models import Categoria, Conta, Movimentacao

class E2EMovimentacaoFlowTest(APITestCase):
    def setUp(self):
        # 1. Criação de um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # URLs da API 
        self.categorias_url = reverse('categoria-list')
        self.contas_url = reverse('conta-list')
        self.movimentacoes_url = reverse('movimentacao-list')

    def test_e2e_full_movimentacao_flow(self):
        # --- PASSO 1: Autenticação (já feita no setUp) ---
        # self.client já está autenticado com o token no setUp

        # --- PASSO 2: Criação de Categoria ---
        categoria_data = {'nome': 'Transporte', 'tipo': 'DESPESA',}
        response_cat = self.client.post(self.categorias_url, categoria_data, format='json')
        self.assertEqual(response_cat.status_code, 201, f"Erro ao criar categoria: {response_cat.data}")
        categoria_id = response_cat.data['id']
        print(f"Categoria criada: {response_cat.data}") # Para debug

        # --- PASSO 3: Criação de Conta ---
        conta_data = {'nome': 'Carteira', 'saldo_inicial': 500.00, }
        response_conta = self.client.post(self.contas_url, conta_data, format='json')
        self.assertEqual(response_conta.status_code, 201, f"Erro ao criar conta: {response_conta.data}")
        conta_id = response_conta.data['id']
        print(f"Conta criada: {response_conta.data}") # Para debug

        # --- PASSO 4: Criação de Movimentação ---
        movimentacao_data = {
            'tipo': 'DESPESA',
            'valor': 75.50,
            'descricao': 'Passagem de ônibus',
            'data': '2025-06-21', # Use uma data válida
            'categoria': categoria_id,
            'conta': conta_id,
        }
        response_mov = self.client.post(self.movimentacoes_url, movimentacao_data, format='json')
        self.assertEqual(response_mov.status_code, 201, f"Erro ao criar movimentação: {response_mov.data}")
        movimentacao_id = response_mov.data['id']
        print(f"Movimentação criada: {response_mov.data}") # Para debug

        # --- PASSO 5: Verificação da Movimentação (Listagem) ---
        response_list = self.client.get(self.movimentacoes_url)
        self.assertEqual(response_list.status_code, 200)
       
        self.assertEqual(len(response_list.data['results']), 1, "Deveria haver 1 movimentação na lista.")
        self.assertEqual(response_list.data['results'][0]['id'], movimentacao_id)
        print(f"Movimentação listada: {response_list.data['results']}") 

        # --- PASSO 6: Atualização da Movimentação ---
        updated_data = {
            'descricao': 'Passagem de ônibus atualizada',
            'valor': 80.00, 
        }
        
        response_update = self.client.patch(reverse('movimentacao-detail', args=[movimentacao_id]), updated_data, format='json')
        self.assertEqual(response_update.status_code, 200, f"Erro ao atualizar movimentação: {response_update.data}")
        self.assertEqual(response_update.data['descricao'], 'Passagem de ônibus atualizada')
        self.assertEqual(float(response_update.data['valor']), 80.00) 
        print(f"Movimentação atualizada: {response_update.data}") 

        # --- PASSO 7: Verificação da Atualização ---
        response_get_updated = self.client.get(reverse('movimentacao-detail', args=[movimentacao_id]))
        self.assertEqual(response_get_updated.status_code, 200)
        self.assertEqual(response_get_updated.data['descricao'], 'Passagem de ônibus atualizada')
        self.assertEqual(float(response_get_updated.data['valor']), 80.00)
        print(f"Movimentação verificada após atualização: {response_get_updated.data}") # Para debug

        # --- PASSO 8: Deleção da Movimentação ---
        response_delete = self.client.delete(reverse('movimentacao-detail', args=[movimentacao_id]))
        self.assertEqual(response_delete.status_code, 204) # 204 No Content para deleção bem-sucedida
        print(f"Movimentação deletada com sucesso.") # Para debug

        # --- PASSO 9: Verificação da Deleção ---
        response_get_deleted = self.client.get(reverse('movimentacao-detail', args=[movimentacao_id]))
        self.assertEqual(response_get_deleted.status_code, 404) 
        response_list_after_delete = self.client.get(self.movimentacoes_url)
        self.assertEqual(len(response_list_after_delete.data['results']), 0, "Nenhuma movimentação deveria existir após a deleção.")
        print(f"Verificação final: Movimentação não encontrada após deleção.") 