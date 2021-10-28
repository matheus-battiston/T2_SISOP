#Matheus Felipe Battiston e Henrique Andreata
class memoria:
    def __init__(self, posicoes, qntdade_particoes):
        self.posicoes = posicoes
        self.qntdade_particoes = qntdade_particoes
        self.tamanho_particao = posicoes/qntdade_particoes
        self.particoes = [None] * qntdade_particoes
        for x in self.particoes:
            x = particao(self.tamanho_particao)
        

class particao:
    def __init__(self,tamanho):
        self.tamanho = tamanho
        self.nao_utilizado = tamanho
        self.ocupado = 0
        self.dados = [None] * tamanho


    def alocar(self,tamanho,id):
        for x in range (0,tamanho):
            self.dados[x] = id
        self.nao_utilizado = self.nao_utilizado - tamanho
def leitura (arquivo):
    
    descricao = []
    arq = open(arquivo)
    linhas = arq.readlines()

    for line in linhas:
        descricao.append(line.replace("\n",''))
    arq.close()
    return descricao

arquivo = "descricao1.txt"
#arquivo = str(input("Digite o nome do arquivo: "))
descricao = leitura(arquivo)
Mem = memoria(8,2)