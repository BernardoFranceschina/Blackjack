from .Mao import *
from .Baralho import *
class Jogador():
    def __init__(self, nome, position):
        self._mao = Mao()
        self._nome = nome
        self._position = position
        self._fichas = 100
        self._apostaAtual = 0
        self._desistiu_rodada = False

    def getDesistencia(self):
        return self._desistiu_rodada
    
    def setDesistencia(self, desistencia = True):
        self._desistiu_rodada = desistencia

    def getMao(self):
        return self._mao.getCartas()

    def resetCartas(self):
        self._mao.resetCartas()

    def getNome(self):
        return self._nome

    def getPosition(self):
        return self._position

    def getAposta(self):
        return self._apostaAtual

    def getFichas(self):
        return self._fichas

    def setAposta(self, aposta):
        self._apostaAtual = int(aposta)
        self._fichas -= int(aposta)

    def avaliarAposta(self, fichas):
        if int(fichas) <= 0:
            return False
        return (int(self._fichas) - int(fichas) >= 0)

    def dobrarAposta(self):
        self._apostaAtual = int(self._apostaAtual) * 2

    def adicionar_fichas(self, valor):
        self._fichas += int(valor)

    def retirar_fichas(self, fichas):
        self._fichas -= int(fichas)

    def devolver_metade_aposta(self):
        self.adicionar_fichas(int(self._apostaAtual) / 2)
        self._apostaAtual = 0
        
    def vitoria(self):
        self.adicionar_fichas(int(self._apostaAtual) * 2)
        self._apostaAtual = 0
    
    def empate(self):
        self.adicionar_fichas(int(self._apostaAtual))
        self._apostaAtual = 0

    def verificarMao(self):
        return self._mao.getValor()

    def adicionarCarta(self, carta: Carta):
        self._mao.adicionaCarta(carta)
