from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Movimentacao, Conta, Categoria
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import MovimentacaoForm, CustomUserCreationForm, CategoriaForm


@login_required
def dashboard(request):
    try:
        conta_usuario = Conta.objects.get(usuario=request.user)
    except Conta.DoesNotExist:
        conta_usuario = Conta.objects.create(usuario=request.user, nome='Conta Principal', saldo=0.00)

    ultimas_movimentacoes = Movimentacao.objects.filter(usuario=request.user).order_by('-data', '-id')[:5]

    context = {
        'saldo_total': conta_usuario.saldo,
        'ultimas_movimentacoes': ultimas_movimentacoes,
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
            movimentacao.usuario = request.user
            movimentacao.save()
            messages.success(request, 'Movimentação adicionada com sucesso!')
            return redirect('financas:lista_movimentacoes')
    else:
        form = MovimentacaoForm(user=request.user)

    context = {
        'form': form,
        'mensagem': 'Adicionar nova movimentação'
    }
    return render(request, 'financas/nova_movimentacao.html', context)

@login_required
def detalhe_movimentacao(request, pk):
    movimentacao = get_object_or_404(Movimentacao, pk=pk, usuario=request.user)
    context = {
        'movimentacao': movimentacao
    }
    return render(request, 'financas/detalhe_movimentacao.html', context)

@login_required
def editar_movimentacao(request, pk):
    movimentacao = get_object_or_404(Movimentacao, pk=pk, usuario=request.user)

    if request.method == 'POST':
        form = MovimentacaoForm(request.POST, user=request.user, instance=movimentacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimentação atualizada com sucesso!')
            return redirect('financas:lista_movimentacoes')
    else:
        form = MovimentacaoForm(user=request.user, instance=movimentacao)

    context = {
        'form': form,
        'movimentacao': movimentacao,
    }
    return render(request, 'financas/nova_movimentacao.html', context)

@login_required
def excluir_movimentacao(request, pk):
    movimentacao = get_object_or_404(Movimentacao, pk=pk, usuario=request.user)

    if request.method == 'POST':
        movimentacao.delete()
        messages.success(request, 'Movimentação excluída com sucesso!')
        return redirect('financas:lista_movimentacoes')

    context = {
        'movimentacao': movimentacao
    }
    return render(request, 'financas/excluir_movimentacao.html', context)

def cadastro_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Sua conta foi criada com sucesso! Bem-vindo(a)!')
            return redirect('financas:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/cadastro_usuario.html', {'form': form})

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.filter(usuario=request.user).order_by('nome')
    context = {
        'categorias': categorias
    }
    return render(request, 'financas/lista_categorias.html', context)

@login_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('financas:lista_categorias')
    else:
        form = CategoriaForm(user=request.user)
    context = {
        'form': form,
        'mensagem': 'Criar Nova Categoria'
    }
    return render(request, 'financas/criar_editar_categoria.html', context)

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('financas:lista_categorias')
    else:
        form = CategoriaForm(instance=categoria, user=request.user)
    context = {
        'form': form,
        'mensagem': 'Editar Categoria',
        'categoria': categoria
    }
    return render(request, 'financas/criar_editar_categoria.html', context)

@login_required
def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, usuario=request.user)

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('financas:lista_categorias')

    context = {
        'categoria': categoria
    }
    return render(request, 'financas/excluir_categoria.html', context)