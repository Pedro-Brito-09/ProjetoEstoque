from collections import deque
import os
import json
from datetime import datetime, timedelta
from Models.Produtos import Produto
from Models.Engradado import Engradado
from Models.Estoque import Estoque
from Models.Pedido import Pedido
from Utils.Data import salvarJSON, carregarJSON, salvarEstoque, carregarEstoque

class SistemaEstoque:
    def __init__(self):
        self.estoque = Estoque()
        self.filaPedidos = deque()
        self.carregarDados()
    
    def carregarDados(self):
        if not os.path.exists("Database"):
            os.makedirs("Database")
        
        self.produtos = carregarJSON("Database/produtos.json", Produto)
        self.historicoPedidos = carregarJSON("Database/pedidos.json", Pedido)
        self.estoque = carregarEstoque("Database/estoque.json")
    
    def salvarDados(self):
        salvarJSON(self.produtos, "Database/produtos.json")
        salvarJSON(self.historicoPedidos, "Database/pedidos.json")
        salvarEstoque(self.estoque, "Database/estoque.json")

    def adicionarProdutoAoEstoque(self):
        print("\n--- Adicionar Produto ao Estoque ---")
        
        dados = {
            'codigo': input("Código do produto: "),
            'lote': input("Número do lote: "),
            'nome': input("Nome do produto: "),
            'peso': float(input("Peso (kg): ")),
            'dataValidade': input("Data de validade (DD-MM-YYYY): "),
            'dataFabricacao': input("Data de fabricação (DD-MM-YYYY): "),
            'precoCompra': float(input("Preço de compra: ")),
            'precoVenda': float(input("Preço de venda: ")),
            'fornecedor': input("Fornecedor: "),
            'fabricante': input("Fabricante: "),
            'categoria': input("Categoria: ")
        }
        
        produto = Produto(**dados)
        quantidade = int(input("Quantidade no engradado: "))
        engradado = Engradado(produto, quantidade)
        
        if self.estoque.adicionarEngradado(engradado):
            self.produtos.append(produto)
            print("Produto adicionado com sucesso!")
            self.salvarDados()
        else:
            print("Não foi possível adicionar o produto.")

    def registrarPedido(self):
        print("\n--- Registrar Novo Pedido ---")
        solicitante = input("Nome do solicitante: ")
        pedido = Pedido(solicitante)
        
        while True:
            codigo = input("Código do produto (ou 'sair' para finalizar): ")
            if codigo.lower() == 'sair':
                break
            
            quantidade = int(input("Quantidade desejada: "))
            pedido.adicionarItem(codigo, quantidade)
        
        self.filaPedidos.append(pedido)
        print("Pedido registrado com sucesso!")
        self.salvarDados()

    def processarPedidos(self):
        print("\n--- Processar Pedidos ---")
        
        if not self.filaPedidos:
            print("Nenhum pedido na fila para processar.")
            return
        
        pedido = self.filaPedidos.popleft()
        print(f"Processando pedido de {pedido.solicitante}")
        
        for item in pedido.itens:
            print(f"\nItem: Código {item.codigoProduto}, Quantidade {item.quantidade}")
            
            produto = None
            for p in self.produtos:
                if p.codigoProduto == item.codigoProduto:
                    produto = p
                    break
            
            if not produto:
                print(f"Produto com código {item.codigoProduto} não encontrado.")
                continue
            
            quantidadeRestante = item.quantidade
            
            while quantidadeRestante > 0:
                pilhaComProduto = None
                for linha in range(8):
                    for coluna in range(5):
                        pilha = self.estoque.matriz[linha][coluna]
                        if not pilha.isVazia() and pilha.topo().produto.codigoProduto == item.codigoProduto:
                            pilhaComProduto = pilha
                            break
                        
                    if pilhaComProduto:
                        break
                
                if not pilhaComProduto:
                    print(f"Estoque insuficiente para o produto {produto.nome}")
                    break
                
                engradado = pilhaComProduto.topo()
                
                if engradado.quantidade > quantidadeRestante:
                    print(f"Removido {quantidadeRestante} unidades de {produto.nome} (restam {engradado.quantidade - quantidadeRestante} no engradado)")
                    engradado.quantidade -= quantidadeRestante
                    quantidadeRestante = 0
                else:
                    print(f"Removido engradado completo de {produto.nome} ({engradado.quantidade} unidades)")
                    quantidadeRestante -= engradado.quantidade
                    pilhaComProduto.removerEngradado()
        
            pedido.atendido = True
            pedido.dataAtendimento = datetime.now()
            self.historicoPedidos.append(pedido)
            print("Pedido processado com sucesso!")
            self.salvarDados()

    def visualizarEstoque(self):
        print("\n--- Visualização do Estoque ---")
        self.estoque.visualizarEstoque()

    def gerarRelatorios(self):
        print("\n--- Gerar Relatórios ---")
        print("1. Produtos próximos ao vencimento")
        print("2. Itens em falta")
        print("3. Histórico de pedidos")
        
        opcao = input("Escolha o relatório: ")
        
        if opcao == "1":
            self.relatorioProdutosProximoVencimento()
        elif opcao == "2":
            self.relatorioItensEmFalta()
        elif opcao == "3":
            self.relatorioHistoricoPedidos()
        else:
            print("Opção inválida.")

    def relatorioProdutosProximoVencimento(self, dias: int = 30):
        print(f"\n--- Produtos próximos ao vencimento (próximos {dias} dias) ---")
        hoje = datetime.now().date()
        limite = hoje + timedelta(days=dias)

        def verificarProdutos(produtos, limite: int, index: int = 0):
            if index >= len(produtos):
                return
            
            produto = produtos[index]
            if produto.dataValidade <= limite:
                diasParaVencer = (produto.dataValidade - hoje).days
                print(f"{produto.nome} - Vence em {diasParaVencer} dias ({produto.dataValidade})")
            
            verificarProdutos(produtos, limite, index + 1)
        
        verificarProdutos(self.produtos, limite)

    def relatorioItensEmFalta(self):
        print("\n--- Itens em falta no estoque ---")
        
        produtosEmEstoque = set()
        for linha in range(8):
            for coluna in range(5):
                pilha = self.estoque.matriz[linha][coluna]
                if not pilha.isVazia():
                    produtosEmEstoque.add(pilha.topo().produto.codigoProduto)
        
        semEstoque = []
        for p in self.produtos:
            if p.codigoProduto not in produtosEmEstoque:
                semEstoque.append(p)

        if not semEstoque:
            print("Nenhum item em falta no estoque.")
        else:
            for produto in semEstoque:
                print(f"{produto.nome} (Código: {produto.codigoProduto})")

    def relatorioHistoricoPedidos(self):
        print("\n--- Histórico de Pedidos ---")

        if not self.historicoPedidos:
            print("Nenhum pedido atendido ainda.")
            return
        
        for i, pedido in enumerate(self.historicoPedidos, 1):
            print(f"\nPedido {i}:")
            print(f"Solicitante: {pedido.solicitante}")
            print(f"Data: {pedido.dataSolicitacao}")
            print("Itens:")

            for item in pedido.itens:
                produto = None
                for p in self.produtos:
                    if p.codigoProduto == item.codigoProduto:
                        produto = p
                        break

                nomeProduto = produto and produto.nome or "Produto não encontrado."
                print(f"- {nomeProduto}: {item.quantidade} unidades")

    def menu(self):
        while True:
            print("\n=== SISTEMA DE ESTOQUE ===")
            print("1. Adicionar produto ao estoque")
            print("2. Registrar pedido")
            print("3. Processar pedidos")
            print("4. Visualizar estoque")
            print("5. Gerar relatórios")
            print("0. Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self.adicionarProdutoAoEstoque()
            elif opcao == "2":
                self.registrarPedido()
            elif opcao == "3":
                self.processarPedidos()
            elif opcao == "4":
                self.visualizarEstoque()
            elif opcao == "5":
                self.gerarRelatorios()
            elif opcao == "0":
                self.salvarDados()
                print("Todos os dados foram salvos.")
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    sistema = SistemaEstoque()
    sistema.menu()