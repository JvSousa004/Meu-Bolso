# Meu Bolso 💰

Um gerenciador de finanças pessoal intuitivo e poderoso, desenvolvido para ajudar você a ter total controle sobre suas receitas e despesas, planejar o futuro e alcançar seus objetivos financeiros!

## Para que serve? ✨

O "Meu Bolso" serve como seu assistente financeiro digital. Ele foi projetado para simplificar a gestão do seu dinheiro, permitindo que você visualize para onde seu dinheiro está indo e de onde ele está vindo. Com ele, você pode:

* **Entender seus hábitos de consumo:** Identifique padrões de gastos e oportunidades de economia.
* **Planejar seu futuro financeiro:** Agende pagamentos e receitas futuras para evitar surpresas.
* **Tomar decisões inteligentes:** Tenha uma visão clara da sua saúde financeira através de relatórios detalhados.

## Funcionalidades Principais 🚀

O "Meu Bolso" está em constante evolução, mas já conta com as seguintes funcionalidades essenciais:

* **Registro de Movimentações:** Cadastre suas receitas e despesas de forma rápida e detalhada, informando valor, data, tipo e categoria.
* **Cálculo Automático de Saldo:** Mantenha seu saldo sempre atualizado após cada movimentação.
* **Classificação por Categorias:** Organize suas transações com categorias personalizadas e utilize-as para filtrar e analisar seus dados.
* **Histórico Completo:** Visualize todo o seu histórico financeiro, com opções de filtragem por período.
* **API RESTful Completa:** Agora com uma API robusta para gerenciamento de movimentações, categorias e contas, permitindo integração com outras aplicações e futuros front-ends (mobile, SPA, etc.).

## Tecnologias Utilizadas 🛠️

### Backend

* **Python:** A linguagem de programação principal, escolhida por sua simplicidade, legibilidade e vasta comunidade.
* **Django:** Um poderoso framework web para Python que acelera o desenvolvimento de aplicações robustas e seguras, seguindo o princípio "Don't Repeat Yourself" (DRY).
* **Django REST Framework (DRF):** Extensão poderosa do Django para a construção de APIs RESTful, fornecendo serializers, viewsets e roteamento automático para agilizar o desenvolvimento da API.

### Frontend

* **Tecnologia:** A interface do usuário é construída utilizando **Django Templates** para renderização server-side (SSR), garantindo uma integração nativa e eficiente com o backend.
* **Estilização e Responsividade:** Adotamos o framework **Bootstrap 5** para a estilização, proporcionando um design moderno, intuitivo e totalmente responsivo, adaptável a diferentes tamanhos de tela.
* **Elementos Visuais:** Para enriquecer a experiência do usuário com ícones e elementos visuais consistentes, utilizamos a biblioteca **Bootstrap Icons**.
* **Experiência do Usuário (UX):** Implementação de feedback visual através do Django Messages Framework e destaque de links ativos na navegação para melhor usabilidade.

## Como Colaborar 🤝

Quer contribuir com o projeto "Meu Bolso"? Ficaremos felizes em receber sua ajuda!

1.  **Faça um Fork** deste repositório.
2.  **Clone o Fork** para sua máquina local:
    ```bash
    git clone [https://github.com/SEU_USUARIO/meu-bolso.git](https://github.com/SEU_USUARIO/meu-bolso.git)
    cd meu-bolso
    ```
3.  **Crie um Ambiente Virtual** e instale as dependências:
    ```bash
    python -m venv venv
    # No Windows PowerShell: .\venv\Scripts\Activate.ps1
    # No Linux/macOS ou Git Bash: source venv/bin/activate
    pip install -r requirements.txt
    ```
    **Nota:** Certifique-se de gerar seu `requirements.txt` atualizado para incluir o `djangorestframework`!

4.  **Crie uma nova Branch** para suas alterações:
    ```bash
    git checkout -b feature/sua-feature-aqui
    ```
5.  **Faça suas alterações** e testes.
6.  **Faça o Commit** de suas mudanças:
    ```bash
    git add .
    git commit -m "feat: Adiciona nova funcionalidade X"
    ```
7.  **Envie para o seu Fork:**
    ```bash
    git push origin feature/sua-feature-aqui
    ```
8.  **Abra um Pull Request** no repositório original descrevendo suas mudanças.

## Integrantes / Desenvolvedores 🧑‍💻

Este projeto está sendo desenvolvido por:

* João Vítor Costa de Sousa - UC23102120
* Gabryel Abrantes - UC23100864
* Esly Victor de Siqueira - UC27101872
* Helder Moreira dos Santos - UC23101992
* Daniel Lima Soares - UC23100050

**Nota:** Este projeto está sendo realizado para entrega do projeto final da matéria **Testes de Software**.

---

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.