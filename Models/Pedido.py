from datetime import datetime

class ItemPedido:
    def __init__(self, codigoProduto: str, quantidade: int):
        self.codigoProduto = codigoProduto
        self.quantidade = quantidade

    def dicionario(self):
        return {
            'codigoProduto': self.codigoProduto,
            'quantidade': self.quantidade
        }

class Pedido:
    def __init__(self, solicitante: str):
        self.solicitante = solicitante
        self.dataSolicitacao = datetime.now()
        self.itens = []
        self.atendido = False
        self.dataAtendimento = None
    
    def adicionarItem(self, codigoProduto: str, quantidade: int):
        self.itens.append(ItemPedido(codigoProduto, quantidade))
    
    def dicionario(self):
        itens = []
        for i in self.itens:
            itens.append(i.dicionario())

        return {
            'solicitante': self.solicitante,
            'dataSolicitacao': self.dataSolicitacao.strftime("%d-%m-%Y %H:%M:%S"),
            'itens': itens,
            'atendido': self.atendido,
            'dataAtendimento': self.dataAtendimento and self.dataAtendimento.strftime("%d-%m-%Y %H:%M:%S") or None
        }

    def __str__(self) -> str:
        return f"Pedido de {self.solicitante} em {self.dataSolicitacao} ({len(self.itens)} itens)"
    
    @classmethod
    def fromDicionario(_, data):
        itens = []
        for i in data["itens"]:
            itens.append(ItemPedido(i["codigoProduto"], i["quantidade"]))

        pedido = Pedido(data["solicitante"])
        pedido.dataSolicitacao = datetime.strptime(data["dataSolicitacao"], "%d-%m-%Y %H:%M:%S")
        pedido.itens = itens
        pedido.atendido = data["atendido"]

        if data["dataAtendimento"]:
            pedido.dataAtendimento = datetime.strptime(data["dataAtendimento"], "%d-%m-%Y %H:%M:%S")

        return pedido