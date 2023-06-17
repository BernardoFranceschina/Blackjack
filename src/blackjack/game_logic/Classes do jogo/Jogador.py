from Mao import *

class Jogador():
    def __init__(self, nome, fichas, mao, vezDeJogar, apostaAtual:int, primeira_jogada:bool, jogando_rodada:bool):
        self._nome = nome
        self._fichas = fichas
        self._mao = Mao()
        self._vezDeJogar = vezDeJogar
        self._apostaAtual = apostaAtual
        self._primeira_jogada = primeira_jogada
        self._jogando_rodada = jogando_rodada


    def turno(self):
        return self._vezDeJogar
    
    def ganhou(self):
        self._fichas += self._apostaAtual * 2
    
    def empatou(self):
        self._fichas += self._apostaAtual 

    def verificarMao(self):
        return self._mao.getValor()

    def Passar_vez(self):
        self._vezDeJogar = False

    def primeira_jogada(self):
        return self._primeira_jogada
    
    def getValor(self):
        return self._fichas
    
    def setJogando_rodada(self):
        pass

