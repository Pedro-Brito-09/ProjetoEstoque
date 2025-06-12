from datetime import datetime

class ItemPedido:
    def __init__(self, codigoProduto: str, quantidade: int):
        self.codigoProduto = codigoProduto
        self.quantidade = quantidade

class Pedido:
    def __init__(self, solicitante: str):
        self.solicitante = solicitante
        self.dataSolicitacao = datetime.now()
        self.itens = []
        self.atendido = False
    
    def adicionarItem(self, codigoProduto: str, quantidade: int):
        self.itens.append(ItemPedido(codigoProduto, quantidade))
    
    def __str__(self) -> str:
        return f"Pedido de {self.solicitante} em {self.dataSolicitacao} ({len(self.itens)} itens)"