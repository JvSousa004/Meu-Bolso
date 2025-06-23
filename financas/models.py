from django.db import models
from django.conf import settings 

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categorias')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ('nome', 'usuario',)

    def __str__(self): 
        return self.nome

class Conta(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conta')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    nome = models.CharField(max_length=100, default="Conta Principal")
  # Nome da conta (ex: "Conta Banco X", "Carteira")

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"

    def __str__(self):
        return f"Conta de {self.usuario.username} - {self.nome}"

    
    def adicionar_receita(self, valor):
        if valor > 0:
            self.saldo += valor
            self.save()

    def subtrair_despesa(self, valor):
        if valor > 0:
            self.saldo -= valor
            self.save() 



class Movimentacao(models.Model):
    # Tipos de movimentação: Receita ou Despesa
    TIPO_MOVIMENTACAO_CHOICES = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimentacoes')
    descricao = models.TextField(blank=True, null=True) 

    
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='movimentacoes_da_conta')


    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ['-data'] # Ordena as movimentações pela data mais recente primeiro

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.valor} em {self.data} ({self.categoria.nome if self.categoria else 'Sem Categoria'})"

   
    def save(self, *args, **kwargs):
       
        if self.conta:
           
            saldo_anterior = 0
            if self.pk: 
                try:
                    old_movimentacao = Movimentacao.objects.get(pk=self.pk)
                    if old_movimentacao.tipo == 'RECEITA':
                        self.conta.subtrair_despesa(old_movimentacao.valor) 
                    else: 
                        self.conta.adicionar_receita(old_movimentacao.valor) 
                except Movimentacao.DoesNotExist:
                    pass 
           
            if self.tipo == 'RECEITA':
                self.conta.adicionar_receita(self.valor)
            elif self.tipo == 'DESPESA':
                self.conta.subtrair_despesa(self.valor)

        super().save(*args, **kwargs) 
    def delete(self, *args, **kwargs):
        if self.conta:
            if self.tipo == 'RECEITA':
                self.conta.subtrair_despesa(self.valor) 
            elif self.tipo == 'DESPESA':
                self.conta.adicionar_receita(self.valor) 
        super().delete(*args, **kwargs) 

