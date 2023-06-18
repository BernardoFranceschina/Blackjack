import json
import random
from .Carta import *
from operator import attrgetter

class Baralho:
    def __init__(self, baralho = []):
        self._baralho = baralho
        self._baralho2 = []

    def criar_baralho(self, primeiro = True, numeros = [], naipes = []):
        self._baralho = []
        if primeiro:
            for numero in Carta.cartasNumeros:
                for naipe in Carta.cartasNaipes:
                    card = Carta(numero, naipe)
                    self._baralho.append(card)
                    self._baralho2.append(card.getCarta())
        else:
            for i in range(len(numeros)):
                card = Carta(numeros[i], naipes[i])
                self._baralho.append(card)
                self._baralho2.append(card.getCarta())

    def embaralhar(self):
        random.shuffle(self._baralho)
        return self._baralho
  
    def getBaralho(self):
        return self._baralho
    
    def getBaralho2(self):
        return self._baralho2