#Matheus Felipe Battiston e Henrique Andreata
class memoria:
    def __init__(self, posicoes, tamanho_particao, politica, fit):
        self.politica = politica
        self.fit = fit
        self.posicoes = posicoes
        self.tamanho_particao = tamanho_particao
        if self.politica == 'PF':
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
        if self.politica == 'PF':
            self.entrar_particaoF(prog,tamanho)
        elif self.fit == 'w' or self.fit == 'W':
            self.entrar_particaoWF(prog,tamanho)
        elif self.fit == 'F' or self.fit == 'f':
            self.entrar_particaoFF(prog,tamanho)
            
            
    def entrar_particaoWF(self,prog,tamanho):
        pass
    
    def entrar_particaoFF(self,prog,tamanho):
        pass
            
    def entrar_particaoF(self,prog,tamanho):
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
        
    def representa_memoria(self):
        auxiliar = 0
        index = 0
        frag = []

        for index, x in enumerate(self.particoes):
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

def printa_memoria(frag):
    for x in frag:
        print( " | ",end = '')
        print(x,end = '')
        
    print (" |")

def execucao(sequencia, Mem):
    frag = Mem.representa_memoria()
    printa_memoria(frag)
    print('========================')  
    
    for linha in sequencia:
        if linha[0] == 'IN':
            Mem.entrar(linha[1][0],linha[1][1])
        elif linha[0] == 'OUT':
            Mem.sair(linha[1])
        print(linha)
        frag = Mem.representa_memoria()
        printa_memoria(frag)
        print("========================")
        input("")      
    
def main():
    arquivo = "descricao1.txt"
    #arquivo = str(input("Digite o nome do arquivo: "))
    descricao = leitura(arquivo)
    politica = str(input("Digite a politica F - partição fixa, V - partição variavel: "))
    if politica == 'F' or politica == 'f':    
        x = int(input("Digite o tamanho da memoria: "))
        y = int(input("Digite o tamanho das partições: "))
        Mem = memoria(x,y,'PF', None)
    elif politica == 'V' or politica == 'v':
        fit = str(input("Voce deseja qual politica de alocação? F - First-Fit W - Worst-Fit"))
        x = int(input("Digite o tamanho da memoria: "))
        Mem = memoria(x,0,'PV',fit)
    execucao(descricao,Mem)
    
if __name__ == "__main__":
    main()