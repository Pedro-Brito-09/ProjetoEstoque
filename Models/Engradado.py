from Models.Produtos import Produto

class Engradado:
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade
    
    def dicionario(self):
        return {
            'produto': self.produto.dicionario(),
            'quantidade': self.quantidade
        }

    def __str__(self) -> str:
        return f"Engradado de {self.produto.nome} ({self.quantidade} unidades)"
    
    @classmethod
    def fromDicionario(_, data):
        produto = Produto(**data['produto'])
        return Engradado(produto, data['quantidade'])