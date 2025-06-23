import re


def calcular_saldo(transacoes):
    return sum([t.valor if t.tipo == 'RECEITA' else -t.valor for t in transacoes])


def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None
