import socket #faz comunicação
import threading #faz multithread
import sys #bblioteca para detectar senalinha e comano,digitamos o IP ou nao (caso tenha Ip, o programa executa o clinte)

class Servidor:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conexoes=[]

        def __init__(self):
            self.sock.bind(('0.0.0.0', 8080))
            self.sock.listen(1)

        def handler(self, conexao,endereco):
            while True:
                dados=conexao.recv(1024)
                for c in self.conexoes:
                    c.send(dados)
                if not dados:
                    print(str(endereco[0]) + ':' + str (endereco[1]) + "Desconectou")
                    self.conexoes.remove(conexao)
                    conexao.close()
                    break

        def run(self):
            while True:
                conexao, endereco = self.sock.accept()
                threadConexao = threading.Thread(target=self.handler, args = (conexao, endereco))
                threadConexao.daemon = True
                threadConexao.start()
                self.conexoes.append(conexao)
                print(str(endereco[0]) + ':' + str(endereco[1]) + "Conectou")

class Cliente:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

    def __init__(self, enderecoServidor):
        self.sock.connect((enderecoServidor, 8080))
        threadInput = threading.Thread(target=self.sendMsg())
        threadInput.daemon = True
        threadInput.start()

        while True:
            dados = self.sock.recv(1024)  #tudo que for recebido na rede será printado tela
            if not dados:
                break
            print(str(dados, 'utf-8'))

if(len(sys.argv)>1):
    client = Cliente(sys.argv[1])
else:
    server = Servidor()
    server.run()

