from Jogador import *
from Dealer import *
from Baralho import *

class Jogo():
    def __init__(self, jogadores: list, baralho: Baralho):
        self._jogadores = jogadores
        self._dealer = Dealer()
        self._baralho = baralho
        self._rodada : int
        self._etapa_aposta :bool
        self._etapa_jogadas :bool
    
    def adicionarValor(self):
        pass
        
    def verificarMao(jogador:Jogador):
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

    def enviarJogada():
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

    def avaliar_aposta(): #fichas, jogador(fichas = jogador.fichas? entao apenas jogador?)
        pass

    def qnt_fichas():
        pass

    def retirar_fichas():
        pass

    def fimTurnoAposta(self):
        self._etapa_aposta = False
        self._etapa_jogadas = True

    def fimTurnoJogadas(self):
        self._etapa_jogadas = False
    
    def receive_hit():
        pass

    def receive_double():
        pass

    def receive_stand():
        pass

    def receive_surrender():
        pass



    
    
    

