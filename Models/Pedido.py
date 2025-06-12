from datetime import datetime

class ItemPedido:
    def __init__(self, codigo_produto: str, quantidade: int):
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade

class Pedido:
    def __init__(self, solicitante: str):
        self.solicitante = solicitante
        self.data_solicitacao = datetime.now()
        self.itens = []
        self.atendido = False
    
    def adicionar_item(self, codigo_produto: str, quantidade: int):
        self.itens.append(ItemPedido(codigo_produto, quantidade))
    
    def __str__(self) -> str:
        return f"Pedido de {self.solicitante} em {self.data_solicitacao} ({len(self.itens)} itens)"