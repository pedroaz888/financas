from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, financial_balance
from extrato.models import Valores
from datetime import datetime
from contas.models import ContaPaga,ContaPagar




def home(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')

    total_livre = total_entradas - total_saidas

    contas = Conta.objects.all()
    
    total_contas = calcula_total(contas, 'valor')

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = financial_balance()

    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas_pagar = ContaPagar.objects.all()
    contas_paga = ContaPaga.objects.all()

    # Contas pagas no mês atual
    contas_pagas_contagem = contas_paga.filter(data_pagamento__month=MES_ATUAL)
  
    contas_vencidas_contagem = contas_pagar.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=[contas_pagas_contagem])
    contas_proximas_contagem = contas_pagar.filter(dia_pagamento__lte=DIA_ATUAL + 5, dia_pagamento__gt=DIA_ATUAL).exclude(id__in=[contas_pagas_contagem])
  


    return render(request, 'home.html', {'contas': contas, 
                                         'total_contas': total_contas,
                                         'total_entradas': total_entradas,
                                         'total_saidas': total_saidas,
                                         'total_livre': total_livre,
                                         'percentual_gastos_essenciais': int(percentual_gastos_essenciais),
                                         'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais),
                                         'contas_vencidas_contagem': contas_vencidas_contagem,
                                         'contas_proximas_contagem': contas_proximas_contagem,})

     
                            




def manage(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    total_contas = calcula_total(contas, 'valor')

    return render(request, 'manage.html', {'contas': contas, 'total_contas': total_contas, 'categorias': categorias})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/manage/')
        
    conta = Conta(
        apelido = apelido,
        banco = banco,
        tipo = tipo,
        valor = valor,
        icone = icone,
    )

    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
    return redirect('/perfil/manage/')

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso')
    return redirect('/perfil/manage/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha o campo nome')
        return redirect('/perfil/manage/')

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/manage/')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    if categoria.essencial:
        categoria.essencial = False
    else:
        categoria.essencial = True

    categoria.save()
    return redirect('/perfil/manage/')


def dashboard(request):
    dados = {}

    categorias = Categoria.objects.all()
    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria=categoria)
        for v in valores:
            total = total + v.valor

        dados[categoria.categoria] = total

    print (dados)


    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 
                                              'values': list(dados.values())})




