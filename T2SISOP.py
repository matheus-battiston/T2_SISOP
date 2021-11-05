#Matheus Felipe Battiston e Henrique Andreata
class memoria:
    def __init__(self, posicoes, tamanho_particao):
        self.posicoes = posicoes
        self.tamanho_particao = tamanho_particao
        self.qntdade_particoes = int(self.posicoes/self.tamanho_particao)
        self.particoes = [None] * self.qntdade_particoes
        for index, x in enumerate(self.particoes):
            self.particoes[index] = particao(self.tamanho_particao)
           
           
    def tem_espaco(self):
        for x in self.particoes:
            if x.ocupado == 0:
                return True
        return False 
    
    def entrar(self, prog,tamanho):
        if self.tem_espaco():
            if int(tamanho) <= self.tamanho_particao:
                for x in self.particoes:
                    if x.ocupado == 0:
                        x.alocar(tamanho,prog[0])
                        break
            else:
                print('Nao foi possivel alocar pelo programa ter tamanho maior que o das partições')
        else:
            print('ESPAÇO INSUFICIENTE DE MEMORIA')
    def sair(self,prog):
        for x in self.particoes:
            if x.ocupado !=0 and x.dados[0] == prog[0]:
                x.liberar()
        
    def printa_memoria(self):
        auxiliar = 0
        index = 0
        frag = []
        for x in self.particoes:
            print(x.dados)
            
        for index, x in enumerate(self.particoes):
            #print(index)
            if x.ocupado == 0:
                auxiliar += self.tamanho_particao
            else:
                auxiliar += x.nao_utilizado
            if int(index) == int(self.qntdade_particoes)-1 and auxiliar != 0:
                frag.append(auxiliar)
                return frag
            if self.particoes[index+1].ocupado == 0:
                pass
            elif auxiliar != 0:
                frag.append(auxiliar)
                auxiliar = 0
            
        return frag
            
        
class particao:
    def __init__(self,tamanho):
        self.tamanho = tamanho
        self.nao_utilizado = tamanho
        self.ocupado = 0
        self.dados = [None] * tamanho


    def alocar(self,tamanho_prog,id):
        tamanho_prog = int(tamanho_prog)
        for x in range (0,tamanho_prog):
            self.dados[x] = id
        self.nao_utilizado = self.nao_utilizado - tamanho_prog
        self.ocupado = self.ocupado + tamanho_prog

    def liberar (self):
        for x in range (0,self.tamanho):
            self.dados[x] = None
        self.nao_utilizado = self.tamanho
        self.ocupado = 0
        
#Funçao que recebe um string, le o arquivo e retorna seu conteudo  
def leitura (arquivo):
    
    descricao = []
    arq = open(arquivo)
    linhas = arq.readlines()

    for line in linhas:
        auxiliar = line.replace("\n",'').replace(')','').split('(')        
        comando = auxiliar[0]
        infos = auxiliar[1].replace(' ','').split(',')
        descricao.append((comando,infos))
    arq.close()
    return descricao

def execucao(sequencia, Mem):
    
    for linha in sequencia:
        frag = Mem.printa_memoria()
        print(frag)

        if linha[0] == 'IN':
            Mem.entrar(linha[1][0],linha[1][1])
        elif linha[0] == 'OUT':
            Mem.sair(linha[1])
        #print(linha)
        
    print(Mem.printa_memoria())

def main():
    arquivo = "descricao1.txt"
    #arquivo = str(input("Digite o nome do arquivo: "))
    descricao = leitura(arquivo)
    # x = int(input("Digite o tamanho da memoria: "))
    # y = int(input("Digite o tamanho das partições: "))
    x = 16
    y = 4
    Mem = memoria(x,y)
    execucao(descricao,Mem)
    
    
    
if __name__ == "__main__":
    main()