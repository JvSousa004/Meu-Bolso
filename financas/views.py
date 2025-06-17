from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse 
from .models import Movimentacao, Conta, Categoria
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login 
from .forms import MovimentacaoForm 

def dashboard(request):
    if not request.user.is_authenticated:
       
        return redirect('login')

    # A partir daqui, sabemos que o usuário está logado
    try:
        conta_usuario = Conta.objects.get(usuario=request.user)
    except Conta.DoesNotExist:
        # Se o usuário não tiver uma conta (o que pode acontecer se ele acabou de ser criado)
        # Por simplicidade, podemos criar uma conta padrão ou redirecionar para uma página de configuração de conta
        conta_usuario = Conta.objects.create(usuario=request.user, nome='Conta Principal', saldo=0.00)


    ultimas_movimentacoes = Movimentacao.objects.filter(usuario=request.user).order_by('-data')[:5]

    context = {
        'saldo_atual': conta_usuario.saldo,
        'ultimas_movimentacoes': ultimas_movimentacoes,
        'nome_usuario': request.user.username
    }
    return render(request, 'financas/dashboard.html', context)

def lista_movimentacoes(request):
    movimentacoes = Movimentacao.objects.filter(usuario=request.user).order_by('-data', '-id')
    context = {
        'movimentacoes': movimentacoes
    }
    return render(request, 'financas/lista_movimentacoes.html', context)

@login_required 
def nova_movimentacao(request):
    if request.method == 'POST':
       
        form = MovimentacaoForm(request.POST, user=request.user)
        if form.is_valid():
            movimentacao = form.save(commit=False) 
            movimentacao.usuario = request.user # Associa a movimentação ao usuário logado
            movimentacao.save() # Agora salva a movimentação
            # RF02: Atualização automática de saldo após cada movimentação
            
            return redirect('financas:lista_movimentacoes') 
    else:
       
        form = MovimentacaoForm(user=request.user)

    context = {
        'form': form,
        'mensagem': 'Adicionar nova movimentação'
    }
    return render(request, 'financas/nova_movimentacao.html', context)

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Opcional: Criar uma conta padrão para o novo usuário
            Conta.objects.create(usuario=user, nome='Conta Principal', saldo=0.00)
            login(request, user) # Loga o usuário automaticamente após o cadastro
            return redirect('financas:dashboard') # Redireciona para o dashboard
    else:
        form = UserCreationForm()
    return render(request, 'registration/cadastro.html', {'form': form}) 


def lista_categorias(request):
    categorias = Categoria.objects.filter(usuario=request.user).order_by('nome')
    context = {
        'categorias': categorias
    }
    return render(request, 'financas/lista_categorias.html', context) 

@login_required
def detalhe_movimentacao(request, pk): # pk é a primary key (ID) da movimentação
    movimentacao = get_object_or_404(Movimentacao, pk=pk, usuario=request.user)
    context = {
        'movimentacao': movimentacao
    }
    return render(request, 'financas/detalhe_movimentacao.html', context)


@login_required
def editar_movimentacao(request, pk): # pk é a primary key (ID) da movimentação
    movimentacao = get_object_or_404(Movimentacao, pk=pk, usuario=request.user)

    if request.method == 'POST':
        # Ao editar, é crucial passar a instância do objeto para o formulário
        # para que ele saiba que está editando, não criando um novo.
        form = MovimentacaoForm(request.POST, user=request.user, instance=movimentacao)
        if form.is_valid():
            # O form.save() vai chamar o método save() sobrescrito no modelo Movimentacao,
            # que já cuida da atualização do saldo, incluindo a reversão do valor antigo.
            form.save()
            return redirect('financas:detalhe_movimentacao', pk=movimentacao.pk) # Redireciona para os detalhes ou lista
    else:
        # Quando a página é carregada (GET), o formulário é pré-preenchido com os dados existentes
        form = MovimentacaoForm(user=request.user, instance=movimentacao)

    context = {
        'form': form,
        'movimentacao': movimentacao, # Passa a movimentação para o template, se necessário
        'mensagem': 'Editar Movimentação'
    }
    return render(request, 'financas/editar_movimentacao.html', context)


@login_required
def excluir_movimentacao(request, pk): # pk é a primary key (ID) da movimentação
    movimentacao = get_object_or_404(Movimentacao, pk=pk, usuario=request.user)

    if request.method == 'POST':
        # O método delete() sobrescrito no modelo Movimentacao já cuida da reversão do saldo.
        movimentacao.delete()
        return redirect('financas:lista_movimentacoes') 
    
   
    context = {
        'movimentacao': movimentacao
    }
    return render(request, 'financas/excluir_movimentacao.html', context)