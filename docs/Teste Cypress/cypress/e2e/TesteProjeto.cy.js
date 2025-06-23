// Prontos, em ordem:

describe('Teste do Software Meu Bolso', () => {

  beforeEach(() => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
  })

  it('Teste: Cadastro Válido', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/');
    cy.get('.mb-0 > a').click()
    cy.get('#id_username').type ('userteste');
    cy.get('#id_password1').type ('12457890j');
    cy.get('#id_password2').type('12457890j');
    cy.get('.btn').click();
    cy.contains('Sua conta foi criada com sucesso! Bem-vindo(a)!').should('be.visible');
  })

  it('Teste: Cadastro com nome inválido', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/');
    cy.get('.mb-0 > a').click()
    cy.get('#id_username').type ('userteste$');
    cy.get('#id_password1').type ('12457890j');
    cy.get('#id_password2').type('12457890j');
    cy.get('.btn').click();
    cy.contains('Enter a valid username').should('be.visible');
  })

it('Teste: Cadastro com senha inválida', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/');
    cy.get('.mb-0 > a').click()
    cy.get('#id_username').type ('userteste5');
    cy.get('#id_password1').type ('12457890');
    cy.get('#id_password2').type('12457890');
    cy.get('.btn').click();
    cy.contains('This password is entirely numeric').should('be.visible');
  })

 it('Teste: Login válido', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
  })

it('Teste: Login inválido', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste10')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.contains('Please enter a correct username and password').should('be.visible');
  })

  it('Teste: Criação de nova categoria', () => {
   cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(2) > .card > .card-body > .btn').click()
    cy.get('.btn-success').click()
    cy.get('#id_nome').type ('Salário')
    cy.get('.card-body > form > .btn').click()
    cy.contains('Categoria criada com sucesso!').should('be.visible');
})

it('Teste: Criação de categoria já existente', () => {
   cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(2) > .card > .card-body > .btn').click()
    cy.get('.btn-success').click()
    cy.get('#id_nome').type ('Salário')
    cy.get('.card-body > form > .btn').click()
    cy.contains('Categoria with this Nome already exists.').should('be.visible');
})

it('Editando nome de Categoria existente', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(2) > .card > .card-body > .btn').click()
    cy.get('.btn-warning > .bi').click()
    cy.get('#id_nome').clear().type ('Mercado')
    cy.get('.card-body > form > .btn').click()
    cy.contains('Categoria atualizada com sucesso!').should('be.visible');
  });

 it('Teste: excluindo Categoria', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(2) > .card > .card-body > .btn').click()
    cy.get(':nth-child(1) > .btn-group > .btn-danger').click()
    cy.get('.btn-danger').click()
    cy.contains('Categoria excluída com sucesso!').should('be.visible');
  });

  it('Teste: Criação de nova categoria (Para conclusão dos testes)', () => {
   cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(2) > .card > .card-body > .btn').click()
    cy.get('.btn-success').click()
    cy.get('#id_nome').type ('Salário')
    cy.get('.card-body > form > .btn').click()
    cy.contains('Categoria criada com sucesso!').should('be.visible');
})

it('Teste: Criando Nova Movimentação (Receita)', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(1) > .card > .card-body > .btn').click()
    cy.get('.btn-success').click()
    cy.get('#id_valor').type ('500')
    cy.get('#id_data').type ('2025-06-23')
    cy.get('#id_categoria').select('Salário');
    cy.get('#id_conta').select('Conta de userteste - Conta Principal')
    cy.get('.card-body > form > .btn').click()
    cy.contains('Movimentação adicionada com sucesso!').should('be.visible');
  });

it('Teste: Criando Nova Movimentação (Despesa)', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(1) > .card > .card-body > .btn').click()
    cy.get('.btn-success').click() 
    cy.get('#id_tipo').select('Despesa')
    cy.get('#id_valor').type ('200')
    cy.get('#id_data').type ('2025-06-23')
    cy.get('#id_categoria').select('Salário'); 
    cy.get('#id_conta').select('Conta de userteste - Conta Principal')
    cy.get('.card-body > form > .btn').click()
    cy.contains('Movimentação adicionada com sucesso!').should('be.visible');
  });

it('Teste: Visualizar uma Movimentação', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(1) > .card > .card-body > .btn').click()
    cy.get(':nth-child(1) > :nth-child(7) > .btn-group > .btn-info').click()
    cy.contains('Detalhes da Movimentação').should('be.visible');
  });

it('Teste: Editar Movimentação (Valor)', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(1) > .card > .card-body > .btn').click()
    cy.get(':nth-child(1) > :nth-child(7) > .btn-group > .btn-warning').click()
    cy.get('#id_valor').clear().type('300');
    cy.get('.card-body > form > .btn').click()
    cy.contains('Movimentação atualizada com sucesso!').should('be.visible');
  });

it('Teste: Apagar Movimentação', () => {
    cy.visit('http://127.0.0.1:8000/accounts/login/')
    cy.get('#id_username').type ('userteste')
    cy.get('#id_password').type ('12457890j')
    cy.get('.btn').click()
    cy.get(':nth-child(1) > .card > .card-body > .btn').click()
    cy.get(':nth-child(1) > :nth-child(7) > .btn-group > .btn-danger').click()
    cy.get('.btn-danger').click()
    cy.contains('Movimentação excluída com sucesso!').should('be.visible');
  });

})