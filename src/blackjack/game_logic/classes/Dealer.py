from .Mao import *

class Dealer():
    def __init__(self):
        self._mao = Mao()

    def verificarMao(self):
        return self._mao.getValor()
    
    def adicionarCarta(self, carta):
        self._mao.adicionaCarta(carta)

    def getMao(self):
        return self._mao.getCartas()