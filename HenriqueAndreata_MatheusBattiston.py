# Alunos: Matheus Felipe Battiston e Henrique Andreata
class Memoria:
    def __init__(self, posicoes, tamanho_particao, politica, fit):
        self.politica = politica
        self.fit = fit
        self.posicoes = posicoes
        self.tamanho_particao = tamanho_particao
        self.particoes = LinkedList()
        if self.politica == 'PF':  # Se a politica for Partição fixa vai calcular a quantidade de partições,
            # criar elas e colocar em uma lista encadeada
            self.qntdade_particoes = int(self.posicoes / self.tamanho_particao)
            for index in range(0, self.qntdade_particoes):
                aux = Particao(self.tamanho_particao, index * tamanho_particao)
                self.particoes.coloca_final(aux)

        else:  # Se a politica for Partições variaveis vai criar uma partição inicial com todas as posições
            aux = Particao(self.posicoes, 0)
            self.particoes.coloca_final(aux)

    # Função para visualização dos resultados. Vai percorrer as partições procurando por fragmentações, retorna uma
    # lista com o tamanho das fragmentações
    def visualizacao(self):
        fragmentacao = []
        auxiliar = 0
        atual = self.particoes.head
        while atual:
            if atual.id == 'H':
                auxiliar += atual.tamanho
            else:
                auxiliar += int(atual.tamanho) - int(atual.utilizado)
            if atual.next is None:
                if auxiliar != 0:
                    fragmentacao.append(auxiliar)
                return fragmentacao
            if atual.next.id == "H":
                pass
            elif auxiliar != 0:
                fragmentacao.append(auxiliar)
                auxiliar = 0
            atual = atual.next

        return fragmentacao

    # ================================================================================================================================

    # Função chamada ao receber o comando "IN", ela chama uma nova função dependendo da politica.
    def entrar(self, prog, tamanho):
        if self.politica == 'PF':
            self.entrar_pf(prog, tamanho)
        if self.politica == 'PV':
            self.entrar_pv(prog, tamanho)

    # Função para colocar um programa na memoria na politica Partições Variaveis
    def entrar_pv(self, prog, tamanho):
        if self.fit == 'W' or self.fit == 'w':
            espaco = self.tem_espaco_worst_fit(tamanho)
        else:
            espaco = self.tem_espaco_first_fit(tamanho)

        if espaco is not False:
            if espaco.tamanho != tamanho:
                nova_part = Particao(espaco.tamanho - int(tamanho), int(espaco.pos_inicial) + int(tamanho))
                espaco.tamanho = int(tamanho)
                espaco.id = prog[0]
                espaco.utilizado = espaco.tamanho
                self.particoes.coloca_apos(espaco, nova_part)
            elif espaco.tamanho == tamanho:
                espaco.id = prog[0]
                espaco.utilizado = espaco.tamanho

        else:
            print("Sem espaço de memoria disponivel ")

    # Função para colocar um programa na memoria na politica Partições Fixas
    def entrar_pf(self, prog, tamanho):
        espaco = self.tem_espaco_part_fixa(tamanho)
        if espaco is not False:
            espaco.utilizado = int(tamanho)
            espaco.id = prog[0]
        else:
            print("Sem espaço de memoria disponivel")

    # Função chamada ao receber o comando 'OUT'. Chama outra função dependendo da politica
    def sair(self, prog):
        if self.politica == 'PF':
            self.sair_pf(prog)
        if self.politica == 'PV':
            self.sair_pv(prog)

    # Função que remove um programa da memoria e faz a junção de duas ou 3 partições caso estejam "lado a lado" e
    # estejam vazias.
    def sair_pv(self, prog):
        atual = self.particoes.head
        while atual:
            ant = atual.last
            prox = atual.next
            if atual.id == prog[0]:
                if ant is not None and ant.id == 'H':  # Testa se a partição anterior existe está vazia
                    if prox is not None and prox.id == 'H':  # Testa se a proxima partição existe e  está vazia
                        ant.next = prox.next
                        ant.tamanho = ant.tamanho + atual.tamanho + prox.tamanho
                        if prox.next is not None:
                            prox.next.last = ant
                        return
                    else:
                        ant.next = prox
                        ant.tamanho += atual.tamanho
                        prox.last = ant
                        return

                elif atual.next is not None and atual.next.id == 'H':  # Testa se a proxima partição existe e está vazia
                    atual.next.last = ant
                    atual.next.tamanho += atual.tamanho
                    if ant is not None:
                        ant.next = atual.next
                    return
                else:  # Se nenhuma partição do lado está vazia não irá se juntar com ninguém e vira um buraco
                    atual.id = 'H'
                    atual.utilizado = 0
                    return
            atual = atual.next

    # Função para remover um programa da memoria na politica de partições variaveis
    def sair_pf(self, prog):
        atual = self.particoes.head
        while atual:
            if atual.id == prog[0]:
                atual.utilizado = 0
                atual.id = 'H'
                return
            atual = atual.next

    # Função para determinar se é possivel alocar espaço para um programa, se não for possivel retorna Falso,
    # se for possivel retorna a partição que será alocado.

    def tem_espaco_part_fixa(self, tamanho):
        atual = self.particoes.head
        while atual:
            if atual.id == 'H' and int(atual.tamanho) >= int(tamanho):
                return atual
            atual = atual.next
        return False

    def tem_espaco_first_fit(self, tamanho):
        atual = self.particoes.head
        menor = None
        if atual.next is None and (atual.id != 'H' or int(atual.tamanho) <= int(tamanho)):
            return False
        while atual:
            if atual.id == 'H' and int(atual.tamanho) >= int(tamanho):
                if menor is None:
                    menor = atual
                elif atual.tamanho < menor.tamanho:
                    menor = atual
            atual = atual.next

        if menor is None:
            return False
        else:
            return menor

    def tem_espaco_worst_fit(self, tamanho):
        atual = self.particoes.head
        maior = None
        if atual.next is None and (atual.id != 'H' or int(atual.tamanho) <= int(tamanho)):
            return False
        while atual:
            if atual.id == 'H' and int(atual.tamanho) >= int(tamanho):
                if maior is None:
                    maior = atual
                elif int(atual.tamanho) > maior.tamanho:
                    maior = atual
            atual = atual.next

        if maior is None:
            return False
        else:
            return maior

        # ================================================================================================================================


# Classe que representa cada partição
class Particao:
    def __init__(self, tamanho, ini):
        self.id = 'H'
        self.tamanho = int(tamanho)
        self.pos_inicial = ini
        self.next = None
        self.last = None
        self.utilizado = 0


# Classe para implementação da lista encadeada
class LinkedList:
    def __init__(self):
        self.head = None

    # Insere um nodo no final da lista encadeada
    def coloca_final(self, part):

        if self.head is None:
            self.head = part
            return

        last = self.head
        while last.next:
            last = last.next

        last.next = part
        part.last = last

    # Insere um nodo após um nodo especifico parassado por parametro e gerencia os "next" e "last"
    @staticmethod
    def coloca_apos(anterior, novo):
        if anterior is None:
            print("the given previous node cannot be NULL")
            return

        new_node = novo
        new_node.next = anterior.next
        anterior.next = new_node
        new_node.last = anterior

        if new_node.next:
            new_node.next.last = new_node


# Funçao que recebe um string, le o arquivo e retorna seu conteudo
def leitura(arquivo):
    descricao = []
    arq = open(arquivo)
    linhas = arq.readlines()

    for line in linhas:
        auxiliar = line.replace("\n", '').replace(')', '').split('(')
        comando = auxiliar[0]
        infos = auxiliar[1].replace(' ', '').split(',')
        descricao.append((comando, infos))
    arq.close()
    return descricao


# Função para formatar a visualização da memoria
def printa_memoria(frag):
    for x in frag:
        print(" | ", end='')
        print(x, end='')

    print(" |")


# Função que vai percorrer a lista de "in's" e "out's" e fazer as respectivas operações, além de chamar as funções
# para visualização do resultado
def execucao(sequencia, mem):
    frag = mem.visualizacao()
    printa_memoria(frag)
    print("========================")
    for linha in sequencia:
        if linha[0] == 'IN':
            print(linha)
            mem.entrar(linha[1][0], linha[1][1])
        elif linha[0] == 'OUT':
            print(linha)
            mem.sair(linha[1])

        frag = mem.visualizacao()
        printa_memoria(frag)
        print("========================")

def main():
    arquivo = str(input("Digite o nome do arquivo: "))
    descricao = leitura(arquivo)
    politica = str(input("Digite a politica F - partição fixa, V - partição variavel: "))
    if politica == 'F' or politica == 'f':
        x = int(input("Digite o tamanho da memoria: "))
        y = int(input("Digite o tamanho das partições: "))
        mem = Memoria(x, y, 'PF', None)
        execucao(descricao, mem)

    elif politica == 'V' or politica == 'v':
        fit = str(input("Voce deseja qual politica de alocação? F - First-Fit, W - Worst-Fit: "))
        x = int(input("Digite o tamanho da memoria: "))
        mem = Memoria(x, 0, 'PV', fit)
        execucao(descricao, mem)


if __name__ == "__main__":
    main()
