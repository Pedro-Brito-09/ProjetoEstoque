from Models.Engradado import Engradado

class Pilha:
    def __init__(self):
        self.engradados = []
        self.capacidadeMaxima = 5
    
    def adicionarEngradado(self, engradado) -> bool:
        if len(self.engradados) < self.capacidadeMaxima:
            self.engradados.append(engradado)
            return True
        
        return False
    
    def removerEngradado(self) -> int | None:
        if not self.isVazia():
            return self.engradados.pop()
        
        return None
    
    def topo(self) -> Engradado:
        if not self.isVazia():
            return self.engradados[-1]
        
        return None
    
    def isVazia(self) -> bool:
        return len(self.engradados) == 0
    
    def isCheia(self) -> bool:
        return len(self.engradados) == self.capacidadeMaxima
    
    def __str__(self) -> str:
        return f"Pilha com {len(self.engradados)} engradados (Capacidade: {self.capacidade_maxima})"