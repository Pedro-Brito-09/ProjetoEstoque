from Models.Produtos import Produto

class Engradado:
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade
    
    def __str__(self):
        return f"Engradado de {self.produto.nome} ({self.quantidade} unidades)"