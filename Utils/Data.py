from datetime import datetime, timedelta
import json
import os

from Models.Estoque import Estoque

def produtosProximoDoVencimento(produtos, dias=30):
    hoje = datetime.now().date()
    limite = hoje + timedelta(days=dias)

    lista = []
    for p in produtos:
        if p.dataValidade <= limite:
            lista.append(p)

    return lista

def salvarJSON(dados, arquivo):
    lista = []
    for d in dados:
        lista.append(d.dicionario())

    with open(arquivo, 'w') as f:
        json.dump(lista, f, indent=2)

def carregarJSON(arquivo, classe):
    if not os.path.exists(arquivo):
        return []
    
    with open(arquivo, 'r') as f:
        dados = json.load(f)

        lista = []
        for d in dados:
            item = None
            fromDicionario = getattr(classe, 'fromDicionario', None)

            if fromDicionario:
                item = fromDicionario(d)
            else:
                item = classe(**d)
            
            lista.append(item)

        return lista

def salvarEstoque(estoque, arquivo):
    with open(arquivo, 'w') as f:
        json.dump(estoque.dicionario(), f, indent=2)

def carregarEstoque(arquivo):
    if not os.path.exists(arquivo):
        return Estoque()
    
    with open(arquivo, 'r') as f:
        dados = json.load(f)
        return Estoque.fromDicionario(dados)