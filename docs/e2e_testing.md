# 🚀 Relatório de Testes E2E com Cypress — *Meu Bolso*

## 📋 Descrição
Este documento apresenta os testes End-to-End (E2E) realizados no sistema **Meu Bolso**, desenvolvido com Django e testado utilizando a ferramenta **Cypress**. O objetivo dos testes é garantir que os principais fluxos do sistema estejam funcionando corretamente, assegurando uma boa experiência ao usuário e a integridade das funcionalidades.

---

## 🔧 Ambiente de Teste

- 🖥️ **Backend:** Django
- 🌐 **Frontend:** HTML + CSS + JS
- 🧪 **Ferramenta de Teste:** Cypress
- 🚀 **Ambiente de Execução:** `http://127.0.0.1:8000`
- 🌍 **Navegador:** Edge

---

## 📑 Cenários de Teste

| ✅ **ID** | 📝 **Cenário**                              | 🔍 **Descrição**                                                           | 🎯 **Resultado Esperado**                                                    |
|------------|---------------------------------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| T01        | Cadastro Válido                             | Cadastro com username e senha válidos                                      | ✔️ Mensagem: *"Sua conta foi criada com sucesso! Bem-vindo(a)!"*             |
| T02        | Cadastro com Nome Inválido                  | Cadastro com username contendo caracteres inválidos                        | ❌ Mensagem: *"Enter a valid username"*                                       |
| T03        | Cadastro com Senha Inválida                 | Cadastro com senha composta apenas por números                             | ❌ Mensagem: *"This password is entirely numeric"*                            |
| T04        | Login Válido                                | Login com username e senha corretos                                        | ✔️ Login realizado com sucesso, redirecionamento para dashboard               |
| T05        | Login Inválido                              | Login com username incorreto                                               | ❌ Mensagem: *"Please enter a correct username and password"*                 |
| T06        | Criar Categoria                             | Criação de uma nova categoria única                                        | ✔️ Mensagem: *"Categoria criada com sucesso!"*                               |
| T07        | Criar Categoria Já Existente                | Tentar criar uma categoria já existente                                    | ❌ Mensagem: *"Categoria with this Nome already exists."*                     |
| T08        | Editar Categoria                            | Alterar o nome de uma categoria existente                                  | ✔️ Mensagem: *"Categoria atualizada com sucesso!"*                           |
| T09        | Excluir Categoria                           | Excluir uma categoria existente                                            | ✔️ Mensagem: *"Categoria excluída com sucesso!"*                             |
| T10        | Criar Movimentação (Receita)                | Criar uma movimentação financeira do tipo receita                          | ✔️ Mensagem: *"Movimentação adicionada com sucesso!"*                        |
| T11        | Criar Movimentação (Despesa)                | Criar uma movimentação financeira do tipo despesa                          | ✔️ Mensagem: *"Movimentação adicionada com sucesso!"*                        |
| T12        | Visualizar Movimentação                     | Acessar os detalhes de uma movimentação registrada                         | ✔️ Página com título: *"Detalhes da Movimentação"*                           |
| T13        | Editar Movimentação (Valor)                 | Alterar o valor de uma movimentação existente                              | ✔️ Mensagem: *"Movimentação atualizada com sucesso!"*                        |
| T14        | Apagar Movimentação                         | Excluir uma movimentação existente                                         | ✔️ Mensagem: *"Movimentação excluída com sucesso!"*                          |

---

## 📸 Evidências dos Testes

- ✅ **Testes executados em modo interativo (`cypress open`)**
- 🎥 Cypress permite também a gravação dos testes (`cypress run --record`)

---

## 🧠 Código dos Testes

Os arquivos dos testes Cypress estão disponíveis na pasta:

```plaintext
/docs/Teste Cypress/cypress/e2e/TesteProjeto.cy.js
