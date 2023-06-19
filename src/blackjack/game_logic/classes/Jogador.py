from .Mao import *
from .Baralho import *
class Jogador():
    def __init__(self, nome, position):
        self._mao = Mao()
        self._nome = nome
        self._position = position
        self._fichas = 100
        self._apostaAtual = 0
        self._vezDeJogar = False
        self._primeira_jogada = False

    def getMao(self):
        return self._mao.getCartas()

    def getNome(self):
        return self._nome

    def getPosition(self):
        return self._position

    def getAposta(self):
        return self._apostaAtual

    def getFichas(self):
        return self._fichas

    def setAposta(self, aposta):
        self._apostaAtual = aposta

    def avaliarAposta(self, fichas):
        if (int(self._fichas) - int(fichas)) >= 0:
            return True
        return False

    def dobrarAposta(self):
        self._apostaAtual = int(self._apostaAtual) * 2

    def adicionar_fichas(self, valor):
        self._fichas += int(valor)

    def retirar_fichas(self, fichas):
        self._fichas -= int(fichas)

    def devolver_metade_aposta(self):
        self.adicionar_fichas(int(self._apostaAtual) / 2)
        self._apostaAtual = 0
        
    def setTurno(self, bool = True):
        self._primeira_jogada = bool
        self._vezDeJogar = bool

    def getTurno(self):
        return self._vezDeJogar
    
    def ganhou(self):
        self._fichas += int(self._apostaAtual) * 2
    
    def empatou(self):
        self._fichas += int(self._apostaAtual)

    def perdeu(self):
        self._fichas -= self._apostaAtual
        self._jogando_rodada = False

    def verificarMao(self):
        return self._mao.getValor()

    def primeira_jogada(self):
        return self._primeira_jogada
    
    def getJogando_rodada(self):
        return self._jogando_rodada
        #Informa se o jogador está jogando a rodada, ou seja, se não efetuou surrender durante a partida


    def adicionarCarta(self, carta: Carta):
        self._mao.adicionaCarta(carta)
