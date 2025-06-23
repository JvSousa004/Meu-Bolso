# 🚀 Relatório de Testes E2E com Cypress

## 📋 Descrição
Este documento apresenta os testes End-to-End (E2E) realizados no sistema **[NOME DO SISTEMA]**, desenvolvido com Django e testado utilizando a ferramenta **Cypress**. O objetivo dos testes é garantir que os principais fluxos do sistema funcionam corretamente, assegurando uma boa experiência ao usuário e a integridade das funcionalidades.

---

## 🔧 Ambiente de Teste

- 🖥️ **Backend:** Django
- 🌐 **Frontend:** HTML + CSS + JS
- 🧪 **Ferramenta de Teste:** Cypress
- 🚀 **Ambiente de Execução:** `http://localhost:8000` (ou outro)
- 🌍 **Navegador:** Chrome / Edge / Electron

---

## 📑 Cenários de Teste

| ✅ **ID** | 📝 **Cenário**                  | 🔍 **Descrição**                                              | 🎯 **Resultado Esperado**                           |
|------------|---------------------------------|---------------------------------------------------------------|------------------------------------------------------|
| T01        | Cadastro Válido                | Preencher todos os campos corretamente e realizar cadastro    | ✔️ Usuário cadastrado com sucesso                    |
| T02        | Cadastro com Senha Inválida    | Senha fora dos padrões permitidos                             | ❌ Mensagem de erro: "Senha inválida"                |
| T03        | Cadastro com Nome Inválido     | Nome menor que 3 caracteres ou com caracteres inválidos       | ❌ Mensagem de erro: "Nome inválido"                 |
| T04        | Login Válido                   | Login com e-mail e senha corretos                             | ✔️ Acesso permitido e mensagem de boas-vindas        |
| T05        | Login Inválido                 | Login com senha incorreta                                     | ❌ Mensagem de erro: "Credenciais inválidas"         |
| T06        | Criar Categoria                | Adicionar uma nova categoria                                  | ✔️ Categoria criada com sucesso                      |
| T07        | Editar Categoria               | Alterar nome de uma categoria existente                       | ✔️ Categoria atualizada com sucesso                  |
| T08        | Excluir Categoria              | Remover uma categoria                                         | ✔️ Categoria excluída com sucesso                    |
| T09        | Criar Movimentação             | Inserir uma nova movimentação financeira                      | ✔️ Movimentação criada com sucesso                   |
| T10        | Visualizar Movimentação        | Verificar se a movimentação aparece na listagem               | ✔️ Movimentação visível na listagem                  |
| T11        | Editar Movimentação            | Alterar dados de uma movimentação existente                   | ✔️ Movimentação atualizada com sucesso               |
| T12        | Excluir Movimentação           | Remover uma movimentação                                      | ✔️ Movimentação excluída com sucesso                 |

---

## 📸 Evidências dos Testes

- ✅ **Testes realizados em modo interativo (`cypress open`)**
- 🎥 Caso configurado, Cypress gera vídeos dos testes (`cypress run --record`)
- 🖼️ **Prints das execuções:** (Adicionar imagens na pasta `/evidencias` ou `/docs` do repositório)

Exemplos de prints recomendados:
- Tela de cadastro bem-sucedido
- Tela com mensagem de erro (senha inválida ou login inválido)
- Tela de movimentação financeira criada
- Tela de categoria editada ou excluída
- Resultado da execução no Cypress (pass/fail dos testes)

---

## 🧠 Código dos Testes

Os arquivos dos testes Cypress estão disponíveis na pasta:

```plaintext
/cypress/e2e/
