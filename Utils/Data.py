from datetime import datetime, timedelta
import json
import os

def produtos_proximo_vencimento(produtos, dias=30):
    hoje = datetime.now().date()
    limite = hoje + timedelta(days=dias)

    lista = []
    for p in produtos:
        if p.data_validade <= limite:
            lista.append(p)

    return lista

def salvar_em_json(dados, arquivo):
    lista = []
    for d in dados:
        lista.append({
            "codigo": d.codigo,
            "lote": d.lote,
            "nome": d.nome,
            "peso": d.peso,
            "dataValidade": "{:%Y-%m-%d}".format(d.dataValidade),
            "dataFabricacao": "{:%Y-%m-%d}".format(d.dataFabricacao),
            "precoCompra": d.precoCompra,
            "precoVenda": d.precoVenda,
            "fornecedor": d.fornecedor,
            "fabricante": d.fabricante,
            "categoria": d.categoria
        })

    with open(arquivo, 'w') as f:
        json.dump(lista, f, indent=2)

def carregar_de_json(arquivo, classe):
    if not os.path.exists(arquivo):
        return []
    
    with open(arquivo, 'r') as f:
        dados = json.load(f)

        lista = []
        for d in dados:
            item = classe(**d)
            lista.append(item)

        return lista