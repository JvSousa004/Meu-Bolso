from django.contrib import admin
from .models import Categoria, Conta, Movimentacao, Planejamento, ListaDeCompras, ItemListaDeCompras

admin.site.register(Categoria)
admin.site.register(Conta)
admin.site.register(Movimentacao)
admin.site.register(Planejamento)
admin.site.register(ListaDeCompras)
admin.site.register(ItemListaDeCompras)