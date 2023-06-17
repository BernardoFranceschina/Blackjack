import random
from Carta import *

class Baralho:
    def __init__(self, baralho = []):
        self._baralho = baralho

    def criar_baralho(self):
        for numero in Carta.cartasNumeros:
            for naipe in Carta.cartasNaipes:
                self._baralho.append(Carta(numero, naipe))

    def embaralhar(self):
        random.shuffle(self._baralho)
        return self._baralho
