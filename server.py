import rpyc
from rpyc.utils.server import ThreadedServer

lista_Cardapio = []

class Cardapio:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

lista_Cardapio.append(Cardapio('Produto A', 2))
lista_Cardapio.append(Cardapio('Produto B', 40))
lista_Cardapio.append(Cardapio('Produto C', 44))
lista_Cardapio.append(Cardapio('Produto D', 67))


class Cantina(rpyc.Service):
    def __init__(self):
        self.msg = ''
        self.cardapio = lista_Cardapio
        self.saldo_cliente = 100

    def exposed_authenticate(self, matricula, senha):
        if matricula == "J123" and senha == "senha123":
            print('Matricula e senha corretos')
            return True
        else:
            print('Matricula e senha incorretos')
            return False

    def exposed_get_cardapio(self):
        cardapio_info = [(item.nome, item.preco) for item in self.cardapio]
        #Testando se o cardapio esta chegando certo até aqui
        #print(cardapio_info)
        return cardapio_info

    def exposed_realizar_venda(self, produto_escolhido):
        produto = None
        for item in self.cardapio:
            if item.nome == produto_escolhido:
                produto = item
                break

        if produto:
            valor_produto = produto.preco
            if self.saldo_cliente >= valor_produto:
                self.saldo_cliente -= valor_produto
                print(f"Venda confirmada! Saldo restante: R${self.saldo_cliente}")
                return self.saldo_cliente
            else:
                print("Saldo insuficiente. Venda cancelada.")
        else:
            print("Produto não encontrado no cardápio.")
            return None


if __name__ == "__main__":
    server = ThreadedServer(Cantina, port=4040)
    print('Servidor rodando na porta 4040')
    server.start()