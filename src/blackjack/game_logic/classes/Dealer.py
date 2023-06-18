from .Mao import *

class Dealer():
    def __init__(self, mao = []):
        self._mao = Mao(mao)

    def verificarMao(self):
        return self._mao.getValor()
    
    def adicionarCarta(self, carta):
        self._mao.adicionaCarta(carta)
        return self._mao