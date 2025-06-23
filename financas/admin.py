from django.contrib import admin
from .models import Categoria, Conta, Movimentacao

admin.site.register(Categoria)
admin.site.register(Conta)
admin.site.register(Movimentacao)
