from django.urls import path
from . import views

app_name = 'financas'

urlpatterns = [
    # Dashboard (Página inicial)
    path('', views.dashboard, name='dashboard'),

    # Rotas de Autenticação personalizadas (cadastro de usuário)
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),

    # Movimentações
    path('movimentacoes/', views.lista_movimentacoes, name='lista_movimentacoes'),
    path('movimentacoes/nova/', views.nova_movimentacao, name='nova_movimentacao'),
    path('movimentacoes/<int:pk>/', views.detalhe_movimentacao, name='detalhe_movimentacao'),
    path('movimentacoes/<int:pk>/editar/', views.editar_movimentacao, name='editar_movimentacao'),
    path('movimentacoes/<int:pk>/excluir/', views.excluir_movimentacao, name='excluir_movimentacao'),

    # Categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'), 
]