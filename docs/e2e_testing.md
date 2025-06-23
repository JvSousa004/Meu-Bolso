# Teste E2E: Fluxo Completo de Gestão de Movimentações

## 1. Objetivo do Teste

Verificar o fluxo completo de interação de um usuário autenticado com a API do "Meu Bolso", garantindo que as operações de criação, listagem, atualização e deleção de **Categorias**, **Contas** e **Movimentações** funcionam de forma integrada e correta, do login à persistência no banco de dados.

## 2. Cenário de Teste Detalhado

Este teste simula um usuário real utilizando a API para gerenciar suas finanças.

**Pré-condições:**
* A aplicação Django está rodando com o banco de dados configurado.
* Um usuário de teste com credenciais válidas existe e pode obter um token de autenticação.

**Passos do Teste:**

1.  **Autenticação:**
    * Um usuário de teste (`testuser`) é criado.
    * Um token de autenticação é gerado para `testuser`.
    * Todas as requisições subsequentes são feitas com este token.

2.  **Criação de Categoria:**
    * É enviada uma requisição `POST` para `/api/categorias/` para criar uma nova categoria (ex: "Transporte", tipo "DESPESA").
    * **Verificação:** A resposta da API deve ser `HTTP 201 Created`, e os dados da categoria criada devem ser retornados com um ID válido.

3.  **Criação de Conta:**
    * É enviada uma requisição `POST` para `/api/contas/` para criar uma nova conta (ex: "Carteira", saldo inicial 500.00).
    * **Verificação:** A resposta da API deve ser `HTTP 201 Created`, e os dados da conta criada devem ser retornados com um ID válido.

4.  **Criação de Movimentação:**
    * É enviada uma requisição `POST` para `/api/movimentacoes/` para criar uma movimentação, utilizando o ID da Categoria e da Conta criadas anteriormente (ex: "Passagem de ônibus", valor 75.50).
    * **Verificação:** A resposta da API deve ser `HTTP 201 Created`, e os dados da movimentação criada devem ser retornados com um ID válido.

5.  **Listagem e Verificação da Movimentação:**
    * É enviada uma requisição `GET` para `/api/movimentacoes/`.
    * **Verificação:** A resposta da API deve ser `HTTP 200 OK`. A lista de resultados paginada deve conter exatamente uma movimentação, e esta movimentação deve corresponder àquela criada no passo anterior (verificando seu ID e alguns campos importantes).

6.  **Atualização da Movimentação:**
    * É enviada uma requisição `PATCH` (ou `PUT`) para `/api/movimentacoes/{id_da_movimentacao}/` para atualizar a movimentação (ex: mudar a descrição para "Passagem de ônibus atualizada" e o valor).
    * **Verificação:** A resposta da API deve ser `HTTP 200 OK`, e a movimentação retornada deve conter os dados atualizados.

7.  **Verificação da Atualização (GET Detalhe):**
    * É enviada uma requisição `GET` para `/api/movimentacoes/{id_da_movimentacao}/` para obter os detalhes da movimentação específica.
    * **Verificação:** A resposta da API deve ser `HTTP 200 OK`, e os dados retornados devem refletir a atualização feita no passo anterior.

8.  **Deleção da Movimentação:**
    * É enviada uma requisição `DELETE` para `/api/movimentacoes/{id_da_movimentacao}/`.
    * **Verificação:** A resposta da API deve ser `HTTP 204 No Content`, indicando sucesso na deleção sem retorno de conteúdo.

9.  **Verificação da Deleção:**
    * É enviada uma requisição `GET` para `/api/movimentacoes/{id_da_movimentacao}/`.
    * **Verificação:** A resposta da API deve ser `HTTP 404 Not Found`, indicando que a movimentação não existe mais.
    * Adicionalmente, é feita uma requisição `GET` para listar todas as movimentações (`/api/movimentacoes/`) para garantir que a lista de resultados esteja vazia (ou não contenha a movimentação deletada).

## 3. Ferramentas Utilizadas

* **Django's `APITestCase`:** Utilizado para simular requisições HTTP e realizar asserções no contexto de testes Django.
* **Django's `reverse`:** Para obter URLs da API de forma dinâmica e robusta.
* **Modelos da Aplicação:** Para criar objetos diretamente no banco de dados de teste (ex: `User`, `Token`, `Categoria`, `Conta`, `Movimentacao`) e verificar o estado do banco.

## 4. Como Rodar o Teste E2E

1.  **Ative seu ambiente virtual:**
    * `.\venv\Scripts\activate` (Windows)
    * `source venv/bin/activate` (Linux/macOS)
2.  **Certifique-se de que o código do teste está no seu projeto:**
    * Cole o código Python do teste (`E2EMovimentacaoFlowTest`) no seu arquivo `financas/tests.py` ou em um novo arquivo como `financas/e2e_tests.py`.
3.  **Execute o teste específico:**
    * Se no `financas/tests.py`:
        ```bash
        python manage.py test financas.tests.E2EMovimentacaoFlowTest
        ```
    * Se em `financas/e2e_tests.py`:
        ```bash
        python manage.py test financas.e2e_tests.E2EMovimentacaoFlowTest
        ```
4.  **Verifique o resultado:** O terminal deve exibir `OK`, indicando que todos os passos do fluxo E2E foram executados com sucesso. Se houver falhas, a mensagem de erro indicará onde o fluxo quebrou.