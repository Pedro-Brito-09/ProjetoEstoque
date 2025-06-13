from datetime import datetime

class Produto:
    def __init__(self, codigo: int, lote: int, nome: str, peso: float, dataValidade: datetime, dataFabricacao: datetime, precoCompra: float, precoVenda: float, fornecedor: str, fabricante: str, categoria: str):
        self.codigoProduto = codigo
        self.lote = lote
        self.nome = nome
        self.peso = peso
        self.dataValidade = datetime.strptime(dataValidade, "%d-%m-%Y").date()
        self.dataFabricacao = datetime.strptime(dataFabricacao, "%d-%m-%Y").date()
        self.precoCompra = precoCompra
        self.precoVenda = precoVenda
        self.fornecedor = fornecedor
        self.fabricante = fabricante
        self.categoria = categoria

    def dicionario(self):
        return {
            "codigo": self.codigoProduto,
            "lote": self.lote,
            "nome": self.nome,
            "peso": self.peso,
            "dataValidade": self.dataValidade.strftime("%d-%m-%Y"),
            "dataFabricacao": self.dataFabricacao.strftime("%d-%m-%Y"),
            "precoCompra": self.precoCompra,
            "precoVenda": self.precoVenda,
            "fornecedor": self.fornecedor,
            "fabricante": self.fabricante,
            "categoria": self.categoria
        }
    
    def __str__(self) -> str:
        return f"{self.nome} (Cód: {self.codigoProduto}, Lote: {self.lote}, Val: {self.dataValidade})"