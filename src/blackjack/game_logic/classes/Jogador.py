from Mao import *
from Baralho import *
class Jogador():
    def __init__(self, nome, position, mao = []):
        self._nome = nome
        self._mao = Mao(mao)
        self._position = position
        self._fichas = 100
        self._apostaAtual = 0
        self._vezDeJogar = False
        self._primeira_jogada = False
        self._jogando_rodada = False

    def turno(self):
        return self._vezDeJogar
    
    def ganhou(self):
        self._fichas += self._apostaAtual * 2
    
    def empatou(self):
        self._fichas += self._apostaAtual 

    def verificarMao(self):
        return self._mao.getValor()

    def passar_vez(self):
        self._vezDeJogar = False

    def primeira_jogada(self):
        return self._primeira_jogada
    
    def getValor(self):
        return self._fichas
    
    def setJogando_rodada(self):
        pass

    def adicionarCarta(self, carta):
        self._mao.adicionaCarta(carta)
        return self._mao

# baralho = Baralho()
# baralho.criar_baralho()
# baralho = baralho.embaralhar()

# jogador = Jogador('B', 1)

# add1 = baralho[:2]
# for i in add1:
#     jogador.adicionarCarta(i)
# print(jogador.verificarMao())

