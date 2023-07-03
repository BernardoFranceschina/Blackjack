import random
from .Carta import *

class Baralho:
    def __init__(self, baralho = []):
        self._baralho = baralho

    def criar_baralho(self, primeiro = True, numeros = [], naipes = []):
        self._baralho = []
        if primeiro:
            for numero in Carta.cartasNumeros:
                for naipe in Carta.cartasNaipes:
                    carta = Carta(numero, naipe)
                    self._baralho.append(carta)
        else:
            for i in range(len(numeros)):
                carta = Carta(numeros[i], naipes[i])
                self._baralho.append(carta)

    def retirar_carta(self):
        return self._baralho.pop()

    def embaralhar(self):
        random.shuffle(self._baralho)
        return self._baralho
  
    def getBaralho(self):
        return self._baralho
