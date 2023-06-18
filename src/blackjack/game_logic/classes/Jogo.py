from .Jogador import *
from .Dealer import *
from .Baralho import *
from .Jogador import *

class Jogo():
    def __init__(self):
        self._dealer = Dealer()
        self._baralho = Baralho()
        self._jogadores = []
        self._rodada: int
        self._etapa_aposta: bool
        self._etapa_jogadas: bool

    def cria_baralho(self):
        self._baralho.criar_baralho()
        return self._baralho.embaralhar()

    def setJogadores(self, jogadores):
        self._jogadores = jogadores


    def verificarMao(jogador: Jogador):
        return jogador.verificarMao() 

    def hit():
        
        pass

    def double():
        pass

    def surrender():
        pass

    def notifica_BlackJack():
        pass

    def notifica_derrota() -> str:
        pass

    def notificar_desistencia():
        pass

    def fim_turno():
        pass

    def devolver_metade_aposta(): #jogador.apostaAtual
        pass

    def retirar_jogador(): #jogador
        pass

    def quantidade_de_jogadores(self):
        return len(self._jogadores)

    def iniciar_partida():
        pass

    def verificar_turno():
        pass

    def avaliar_aposta(self, fichas, position): #fichas, jogador(fichas = jogador.fichas? entao apenas jogador?)
        jogador = self.jogadores[position]
        if fichas <= jogador.fichas:
            jogador.fichas -= fichas
            if position == len(self._jogadores) - 1:
                #vai distribuir as cartas
                self._etapa_aposta = False
            return "Aposta feita com sucesso"
        else:
            return "Fichas Insuficientes"


    def fimTurnoAposta(self):
        self._etapa_aposta = False
        self._etapa_jogadas = True

    def fimTurnoJogadas(self):
        self._etapa_jogadas = False
    
    def receive_hit(self, jogador):
        pass

    def receive_double(self, jogador):
        pass

    def receive_stand(self, jogador):
        pass

    def receive_surrender(self, jogador):
        pass

    def receber_carta_jogador(self, jogador):
        pass

    def receber_carta_dealer(self):
        pass
