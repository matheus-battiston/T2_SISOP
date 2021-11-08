class memoria:
    def __init__(self, posicoes, tamanho_particao, politica, fit):
        self.politica = politica
        self.fit = fit
        self.posicoes = posicoes
        self.tamanho_particao = tamanho_particao
        self.particoes = LinkedList()
        if self.politica == 'PF':
            self.qntdade_particoes = int(self.posicoes/self.tamanho_particao)
            for index in range (0,self.qntdade_particoes):
                aux = particao(self.tamanho_particao,index*tamanho_particao)
                self.particoes.coloca_final(aux)
           
        else:
            aux = particao(self.posicoes,0)
            self.particoes.coloca_final(aux)
            
           
    def visualizacao(self):
        frag = []
        auxiliar = 0
        atual = self.particoes.head
        while (atual):
            if atual.id == 'H':
                auxiliar += atual.tamanho
            else:
                auxiliar += int(atual.tamanho) - int(atual.utilizado)      
            if atual.next is None and auxiliar != 0:
                frag.append(auxiliar)
                return frag   
            if atual.next.id == "H":
                pass        
            elif auxiliar != 0:
                frag.append(auxiliar)
                auxiliar = 0                
            atual = atual.next
            
        return frag
                  
    def tem_espaco(self,tamanho):
        atual = self.particoes.head
        while(atual):
            if atual.id == 'H' and int(atual.tamanho) >= int(tamanho):
                return atual
            atual = atual.next
        return False
                
    def entrar(self,prog,tamanho):
        if self.politica == 'PF':
            self.entrar_PF(prog,tamanho)
        if self.politica == 'PV':
            self.entrar_PV(prog,tamanho)
            
    def entrar_PV(self,prog,tamanho):
        espaco = self.tem_espaco(tamanho)
        if espaco != False:
            nova_part = particao(espaco.tamanho -int(tamanho), int(espaco.pos_inicial) + int(tamanho))
            espaco.tamanho = int(tamanho)
            espaco.id = prog[0]
            espaco.utilizado = espaco.tamanho
            self.particoes.coloca_apos(espaco,nova_part)
                
        else:
            print("Sem espaço de memoria disponivel ")
            
            
    def entrar_PF(self,prog,tamanho):
        espaco = self.tem_espaco(tamanho)
        if espaco != False:
            espaco.utilizado = int(tamanho)
            espaco.id = prog[0]
        else:
            print( "Sem espaço de memoria disponivel")


    def sair(self,prog):
        if self.politica == 'PF':
            self.sair_PF(prog)
        if self.politica == 'PV':
            self.sair_PV(prog)
            
            
    def sair_PV(self,prog):
        atual = self.particoes.head
        while (atual):
            ant = atual.last
            prox = atual.next
            if atual.id == prog[0]:
                if ant != None and ant.id == 'H':
                    if prox != None and prox.id== 'H':
                        ant.next = prox.next
                        ant.tamanho = ant.tamanho + atual.tamanho + prox.tamanho
                        if prox.next != None:
                            prox.next.last = ant
                        return
                    else:
                        ant.next = prox
                        ant.tamanho += atual.tamanho
                        prox.last = ant
                        return
                        
                elif atual.next != None and atual.next.id == 'H':
                    atual.next.last = ant
                    atual.next.tamanho += atual.tamanho
                    ant.next = atual.next
                    return
                else:
                    atual.id = 'H'
                    atual.utilizado = 0
                    return
            atual = atual.next
                
        
    def sair_PF(self,prog):
        atual = self.particoes.head
        while(atual):
            if atual.id == prog[0]:
                atual.utilizado = 0
                atual.id = 'H'
                return
            atual = atual.next
        
         
class LinkedList:
    def __init__(self):  
        self.head = None
  
    def insert(self, part):
        if(self.head):
            current = self.head
            while(current.next):
                current = current.next
            current.next = part
        else:
            self.head = part
      
    def coloca_final(self, part):

        if self.head is None:
            self.head = part
            return
 
        last = self.head
        while last.next:
            last = last.next
 
        last.next = part
        part.last = last
       
    def printLL(self):
        current = self.head
        while(current):
            print(current.id)
            current = current.next
            
    def coloca_apos(self,anterior,novo):
        if anterior is None:
            print("the given previous node cannot be NULL")
            return
 
        new_node = novo
        new_node.next = anterior.next
        anterior.next = new_node
        new_node.last = anterior
 
        if new_node.next:
            new_node.next.last = new_node
  
class particao:
    def __init__(self,tamanho,ini,next=None,last = None):
        self.id = 'H'
        self.tamanho = int(tamanho)
        self.pos_inicial = ini
        self.next = next
        self.last = last
        self.utilizado = 0
        
        
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

#Função para formatar a visualização da memoria
def printa_memoria(frag):
    for x in frag:
        print( " | ",end = '')
        print(x,end = '')
        
    print (" |")

#Função que vai percorrer a lista de "in's" e "out's" e fazer as respectivas operações
def execucao(sequencia,Mem):
    frag = Mem.visualizacao()  
    printa_memoria(frag)
    print("========================")
    for linha in sequencia:
        if linha[0] == 'IN':
            print(linha)
            Mem.entrar(linha[1][0],linha[1][1])
        elif linha[0] == 'OUT':
            print(linha[1])
            Mem.sair(linha[1])   

        frag = Mem.visualizacao()  
        printa_memoria(frag)
        print("========================")
        input("")      


def main():
    global LL
    arquivo = "descricao3.txt"
    #arquivo = str(input("Digite o nome do arquivo: "))
    descricao = leitura(arquivo)
    politica = str(input("Digite a politica F - partição fixa, V - partição variavel: "))
    if politica == 'F' or politica == 'f':    
        x = int(input("Digite o tamanho da memoria: "))
        y = int(input("Digite o tamanho das partições: "))
        Mem = memoria(x,y,'PF', None)
        execucao(descricao,Mem)

    elif politica == 'V' or politica == 'v':
        fit = str(input("Voce deseja qual politica de alocação? F - First-Fit W - Worst-Fit: "))
        x = int(input("Digite o tamanho da memoria: "))
        Mem = memoria(x,0,'PV',fit)
        execucao(descricao,Mem)

    

if __name__ == "__main__":
    main()       