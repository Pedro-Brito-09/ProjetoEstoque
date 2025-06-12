from Models.Pilha import Pilha
from Models.Engradado import Engradado
from Models.Produtos import Produto

class Estoque:
    def __init__(self):
        self.matriz = []

        for i in range(5):
            for j in range(8):
                self.matriz.append(Pilha())
    
    def acharPilhaParaColocarProduto(self, produto: Produto) -> tuple[int, int] | None:
        for linha in range(8):
            for coluna in range(5):
                pilha = self.matriz[linha][coluna]
                topo = pilha.topo()
                if topo and topo.produto.codigo == produto.codigo and not pilha.isCheia():
                    return (linha, coluna)
        
        for linha in range(8):
            for coluna in range(5):
                if self.matriz[linha][coluna].isVazia():
                    return (linha, coluna)
        
        return None
    
    def adicionarEngradado(self, engradado: Engradado) -> bool:
        posicao = self.acharPilhaParaColocarProduto(engradado.produto)

        if posicao:
            linha, coluna = posicao
            return self.matriz[linha][coluna].adicionarEngradado(engradado)
        
        return False
    
    def removerEngradadoPorProduto(self, codigoProduto: int) -> int | None:
        for linha in range(7, -1, -1):
            for coluna in range(4, -1, -1):
                pilha = self.matriz[linha][coluna]
                topo = pilha.topo()

                if topo and topo.produto.codigo == codigoProduto:
                    return pilha.removerEngradado()
                
        return None
    
    def visualizarEstoque(self):
        for linha in range(8):
            for coluna in range(5):
                pilha = self.matriz[linha][coluna]
                print(f"Posição [{linha}][{coluna}]: {pilha}")

                if not pilha.isVazia():
                    print(f"  Topo: {pilha.topo()}")