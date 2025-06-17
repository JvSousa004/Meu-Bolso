from django.urls import path
from . import views

app_name = 'financas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('movimentacoes/', views.lista_movimentacoes, name='lista_movimentacoes'),
    path('movimentacoes/nova/', views.nova_movimentacao, name='nova_movimentacao'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'), 
     path('movimentacoes/<int:pk>/', views.detalhe_movimentacao, name='detalhe_movimentacao'),
    path('movimentacoes/<int:pk>/editar/', views.editar_movimentacao, name='editar_movimentacao'),
    path('movimentacoes/<int:pk>/excluir/', views.excluir_movimentacao, name='excluir_movimentacao'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
]