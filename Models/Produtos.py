from datetime import datetime

class Produto:
    def __init__(self, codigo: int, lote: int, nome: str, peso: float, dataValidade: datetime, dataFabricacao: datetime, precoCompra: float, precoVenda: float, fornecedor: str, fabricante: str, categoria: str):
        self.codigo = codigo
        self.lote = lote
        self.nome = nome
        self.peso = peso
        self.dataValidade = datetime.strptime(dataValidade, "%Y-%m-%d").date()
        self.dataFabricacao = datetime.strptime(dataFabricacao, "%Y-%m-%d").date()
        self.precoCompra = precoCompra
        self.precoVenda = precoVenda
        self.fornecedor = fornecedor
        self.fabricante = fabricante
        self.categoria = categoria
    
    def __str__(self) -> str:
        return f"{self.nome} (Cód: {self.codigo}, Lote: {self.lote}, Val: {self.dataValidade})"