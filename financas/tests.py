import pytest
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from financas.utils import calcular_saldo, validar_email
from financas.models import Conta, Movimentacao
from financas.forms import MovimentacaoForm
from collections import namedtuple

# TESTE 1 – Criar movimentação no banco


@pytest.mark.django_db
def test_criar_movimentacao():
    usuario = User.objects.create_user(
        username='usuario_teste', password='senha123')
    conta = Conta.objects.create(usuario=usuario, saldo=0, nome="Conta Teste")

    movimentacao = Movimentacao.objects.create(
        usuario=usuario,
        tipo='RECEITA',
        valor=100,
        data='2025-06-21',
        conta=conta,
        descricao="Depósito de teste"
    )

    assert Movimentacao.objects.filter(descricao="Depósito de teste").exists()

# TESTE 2 – Formulário válido


@pytest.mark.django_db
def test_formulario_valido():
    usuario = User.objects.create_user(
        username='usuario_form', password='senha123')
    conta = Conta.objects.create(usuario=usuario, saldo=0, nome="Conta Teste")

    form_data = {
        'usuario': usuario.id,
        'tipo': 'RECEITA',
        'valor': 150,
        'data': '2025-06-21',
        'conta': conta.id,
        'descricao': 'Salário'
    }

    form = MovimentacaoForm(data=form_data)
    assert form.is_valid()

# TESTE 3 – Cálculo de saldo


def test_calculo_saldo():
    TransacaoFake = namedtuple('Transacao', ['valor', 'tipo'])
    transacoes = [
        TransacaoFake(valor=100, tipo='RECEITA'),
        TransacaoFake(valor=50, tipo='DESPESA'),
        TransacaoFake(valor=25, tipo='RECEITA'),
    ]
    resultado = calcular_saldo(transacoes)
    assert resultado == 75

# TESTE 4 – Validação de e-mail


@pytest.mark.parametrize("email, esperado", [
    ("user@example.com", True),
    ("invalido@", False),
    ("", False),
])
def test_validar_email(email, esperado):
    assert validar_email(email) == esperado

# TESTE 5 – Login de usuário


@pytest.mark.django_db
def test_login_usuario(client):
    user = User.objects.create_user(
        username='usuario_login', password='senha123')
    login = client.login(username='usuario_login', password='senha123')
    assert login == True

# TESTE 6 – Tentar criar movimentação sem conta (erro esperado)


@pytest.mark.django_db
def test_movimentacao_sem_conta():
    usuario = User.objects.create_user(
        username='usuario_erro', password='senha123')

    with pytest.raises(Movimentacao.conta.RelatedObjectDoesNotExist):
        Movimentacao.objects.create(
            usuario=usuario,
            tipo='RECEITA',
            valor=50,
            data='2025-06-21',
            descricao="Teste sem conta"
        )

# TESTE 7 – Criar categoria


@pytest.mark.django_db
def test_criar_categoria():
    usuario = User.objects.create_user(
        username='user_cat', password='senha123')
    from financas.models import Categoria
    categoria = Categoria.objects.create(nome='Alimentação', usuario=usuario)
    assert Categoria.objects.filter(
        nome='Alimentação', usuario=usuario).exists()

# TESTE 8 – Visualizar categorias


@pytest.mark.django_db
def test_visualizar_categorias():
    usuario = User.objects.create_user(
        username='user_cat_list', password='senha123')
    from financas.models import Categoria
    Categoria.objects.create(nome='Transporte', usuario=usuario)
    categorias = Categoria.objects.filter(usuario=usuario)
    assert categorias.count() == 1

# TESTE 9 – Editar categoria


@pytest.mark.django_db
def test_editar_categoria():
    usuario = User.objects.create_user(
        username='user_cat_edit', password='senha123')
    from financas.models import Categoria
    categoria = Categoria.objects.create(nome='Lazer', usuario=usuario)
    categoria.nome = 'Lazer Editado'
    categoria.save()
    categoria.refresh_from_db()
    assert categoria.nome == 'Lazer Editado'

# TESTE 10 – Excluir categoria


@pytest.mark.django_db
def test_excluir_categoria():
    usuario = User.objects.create_user(
        username='user_cat_del', password='senha123')
    from financas.models import Categoria
    categoria = Categoria.objects.create(nome='Saúde', usuario=usuario)
    categoria.delete()
    assert not Categoria.objects.filter(nome='Saúde', usuario=usuario).exists()

# TESTE 11 – Criar movimentação (CRUD)


@pytest.mark.django_db
def test_criar_movimentacao_crud():
    usuario = User.objects.create_user(
        username='user_mov_create', password='senha123')
    conta = Conta.objects.create(usuario=usuario, saldo=0, nome='Conta Teste')
    movimentacao = Movimentacao.objects.create(
        usuario=usuario,
        tipo='RECEITA',
        valor=200,
        data='2025-06-21',
        conta=conta,
        descricao='Salário'
    )
    assert Movimentacao.objects.filter(
        descricao='Salário', usuario=usuario).exists()

# TESTE 12 – Visualizar movimentações


@pytest.mark.django_db
def test_visualizar_movimentacoes():
    usuario = User.objects.create_user(
        username='user_mov_list', password='senha123')
    conta = Conta.objects.create(usuario=usuario, saldo=0, nome='Conta Teste')
    Movimentacao.objects.create(
        usuario=usuario,
        tipo='DESPESA',
        valor=80,
        data='2025-06-21',
        conta=conta,
        descricao='Supermercado'
    )
    movimentacoes = Movimentacao.objects.filter(usuario=usuario)
    assert movimentacoes.count() == 1

# TESTE 13 – Editar movimentação


@pytest.mark.django_db
def test_editar_movimentacao():
    usuario = User.objects.create_user(
        username='user_mov_edit', password='senha123')
    conta = Conta.objects.create(usuario=usuario, saldo=0, nome='Conta Teste')
    movimentacao = Movimentacao.objects.create(
        usuario=usuario,
        tipo='DESPESA',
        valor=50,
        data='2025-06-21',
        conta=conta,
        descricao='Padaria'
    )
    movimentacao.valor = 100
    movimentacao.save()
    movimentacao.refresh_from_db()
    assert movimentacao.valor == 100

# TESTE 14 – Excluir movimentação


@pytest.mark.django_db
def test_excluir_movimentacao():
    usuario = User.objects.create_user(
        username='user_mov_del', password='senha123')
    conta = Conta.objects.create(usuario=usuario, saldo=0, nome='Conta Teste')
    movimentacao = Movimentacao.objects.create(
        usuario=usuario,
        tipo='RECEITA',
        valor=300,
        data='2025-06-21',
        conta=conta,
        descricao='Freelance'
    )
    movimentacao.delete()
    assert not Movimentacao.objects.filter(
        descricao='Freelance', usuario=usuario).exists()
