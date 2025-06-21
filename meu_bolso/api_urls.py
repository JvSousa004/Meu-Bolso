from rest_framework.routers import DefaultRouter
from django.urls import path, include


from financas.api_views import MovimentacaoViewSet, CategoriaViewSet, ContaViewSet


router = DefaultRouter()


router.register(r'movimentacoes', MovimentacaoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'contas', ContaViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]