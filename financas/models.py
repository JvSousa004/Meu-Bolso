from django.db import models
from django.conf import settings

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categorias')

# O próprio usuário do app vai fazer o CRUD da "categoria financeira". Atende o RF4

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
    descricao = models.TextField(blank=True, null=True) # Campo opcional como você pediu

    # Adicionar o campo de conta à qual a movimentação pertence
    # Isso é crucial para saber qual saldo deve ser afetado
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='movimentacoes_da_conta')


    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ['-data'] # Ordena as movimentações pela data mais recente primeiro

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.valor} em {self.data} ({self.categoria.nome if self.categoria else 'Sem Categoria'})"

    # Sobrescrevendo o método save() para atualizar o saldo da conta
    def save(self, *args, **kwargs):
        # Para garantir que a conta exista e tenha saldo para atualizar
        if self.conta:
            # Recuperar o objeto da conta antes de salvar a movimentação
            # para comparar o valor antigo em caso de atualização
            saldo_anterior = 0
            if self.pk: # Se for uma atualização de um objeto existente
                try:
                    old_movimentacao = Movimentacao.objects.get(pk=self.pk)
                    if old_movimentacao.tipo == 'RECEITA':
                        self.conta.subtrair_despesa(old_movimentacao.valor) # Remove o valor antigo como se fosse uma despesa
                    else: # 'DESPESA'
                        self.conta.adicionar_receita(old_movimentacao.valor) # Adiciona o valor antigo como se fosse uma receita
                except Movimentacao.DoesNotExist:
                    pass # É uma nova movimentação, então não há saldo anterior para subtrair

            # Agora aplica o novo valor
            if self.tipo == 'RECEITA':
                self.conta.adicionar_receita(self.valor)
            elif self.tipo == 'DESPESA':
                self.conta.subtrair_despesa(self.valor)

        super().save(*args, **kwargs) # Chama o método save original da classe pai

    # Sobrescrevendo o método delete() para reajustar o saldo da conta
    def delete(self, *args, **kwargs):
        if self.conta:
            if self.tipo == 'RECEITA':
                self.conta.subtrair_despesa(self.valor) # Se uma receita for deletada, subtrai o valor do saldo
            elif self.tipo == 'DESPESA':
                self.conta.adicionar_receita(self.valor) # Se uma despesa for deletada, adiciona o valor de volta ao saldo
        super().delete(*args, **kwargs) 

class Planejamento(models.Model):
    # Escolhas para o tipo de agendamento (Receita ou Despesa)
    TIPO_AGENDAMENTO_CHOICES = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]

    # Escolhas para a frequência do agendamento
    FREQUENCIA_CHOICES = [
        ('UNICO', 'Único'),
        ('DIARIO', 'Diário'),
        ('SEMANAL', 'Semanal'),
        ('MENSAL', 'Mensal'),
        ('ANUAL', 'Anual'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='planejamentos')
    tipo = models.CharField(max_length=7, choices=TIPO_AGENDAMENTO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_agendada = models.DateField()
    frequencia = models.CharField(max_length=10, choices=FREQUENCIA_CHOICES, default='UNICO')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='planejamentos')
    descricao = models.TextField(blank=True, null=True)

    # Status do agendamento (para controle se já foi realizado/pago, etc.)
    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('REALIZADO', 'Realizado'),
        ('CANCELADO', 'Cancelado'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AGENDADO')

    # A movimentação real que foi criada a partir deste planejamento (se houver)
    # Isso ajuda a vincular o agendamento à transação efetiva.
    movimentacao_gerada = models.OneToOneField(
        'Movimentacao',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planejamento_origem'
    )

    class Meta:
        verbose_name = "Planejamento"
        verbose_name_plural = "Planejamentos"
        ordering = ['data_agendada'] # Ordena os planejamentos pela data agendada

    def __str__(self):
        return f"Agendamento: {self.get_tipo_display()} de {self.valor} em {self.data_agendada} ({self.get_frequencia_display()})"

    # Podemos adicionar um método aqui para "converter" um planejamento em uma movimentação
    # Este método seria chamado por uma view ou por uma tarefa agendada (futuramente)
    def realizar_movimentacao(self, conta_destino: 'Conta'):
        # Verifica se o planejamento ainda não foi realizado e se a data já chegou
        if self.status == 'AGENDADO' and self.data_agendada <= models.DateField.today():
            movimentacao = Movimentacao.objects.create(
                usuario=self.usuario,
                tipo=self.tipo,
                valor=self.valor,
                data=models.DateField.today(), # A data da movimentação real pode ser a de hoje
                categoria=self.categoria,
                descricao=f"Movimentação gerada do planejamento: {self.descricao or self.get_tipo_display()}",
                conta=conta_destino
            )
            self.movimentacao_gerada = movimentacao
            self.status = 'REALIZADO'
            self.save()
            return movimentacao
        return None