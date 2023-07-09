from extrato.models import Valores
from datetime import datetime


def calcula_total(obj, campo):
    total = 0
    for i in obj:
        total += getattr(i, campo)
    return total


def financial_balance():
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)

    total_gastos_essenciais = calcula_total(gastos_essenciais, 'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor')

    total = total_gastos_essenciais + total_gastos_nao_essenciais

    try:
        percentual_gastos_essenciais = total_gastos_essenciais * 100 / total
        percentual_nao_gastos_essenciais = total_gastos_nao_essenciais * 100 / total
        return percentual_gastos_essenciais, percentual_nao_gastos_essenciais
    except:
        return 0, 0
  







#PODERIA USAR ISSO DENTRO DA FUNÇÃO --------------------------------------------------------
""" total_contas = 0
    for conta in contas:
        total_contas +=  conta.valor """