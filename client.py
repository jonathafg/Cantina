import rpyc

class AutenticacaoCliente:
    def __init__(self):
        self.conn = rpyc.connect('localhost', 4040)

    def autentica(self, matricula, senha):
        autenticado = self.conn.root.exposed_authenticate(matricula, senha)
        return autenticado

    def exibir_cardapio(self):
        cardapio = self.conn.root.exposed_get_cardapio()
        #Testando se o cardapio esta chegando normal até aqui 
        #print (cardapio) 
        return cardapio

    def realizar_venda(self, produto_escolhido):
        novo_saldo = self.conn.root.exposed_realizar_venda(produto_escolhido)
        return novo_saldo

if __name__ == "__main__":
    client = AutenticacaoCliente()
    matricula = "J123"
    senha = "senha123"

    autenticado = client.autentica(matricula, senha)

    if autenticado:
        print("Autenticado com sucesso!")
        cardapio = client.exibir_cardapio()
        print("Cardápio:")
        for item in cardapio:
            nome, preco = item
            print(f"{nome}: R${preco}")

        produto_escolhido = input("Escolha um produto: ")

        novo_saldo = client.realizar_venda(produto_escolhido)
        if novo_saldo is not None:
            print(f"Saldo atual: R${novo_saldo}")
        else:
            print("Produto não encontrado no Cardápio")