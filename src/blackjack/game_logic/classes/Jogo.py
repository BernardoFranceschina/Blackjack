from .Jogador import *
from .Dealer import *
from .Baralho import *
from .Jogador import *

class Jogo():
    def __init__(self):
        self._baralho = Baralho()
        self._dealer = Dealer()
        self._jogadores = []
        self._rodada = 1
        self._jogador_jogando = 0
        self._etapa_jogadas = False
        self._etapa_aposta = False
        self._etapa_jogadaDealer = False

    def criarBaralho(self, primeiro = True, numeros = [], naipes = []):
        self._baralho.criar_baralho(primeiro, numeros, naipes)

    def getRodada(self):
        return self._rodada

    def criaNotificacao(self, jogada, local, resultado, position):
        jogador = self.getJogadorByPosition(position)
        if local == 1:
            notificacao = f'{jogada}\nVocê '
        else:
            notificacao = f'{jogada}\n{jogador.getNome()} '

        if resultado == 'blackjack':
            notificacao += "fez um blackjack"
        else:
            notificacao += resultado
        return notificacao
        
    # -------------------------------------------------------------

    def resetJogo(self):
        self._baralho = Baralho()
        self._dealer = Dealer()
        self._jogadores = []
        self._rodada = 1
        self._jogador_jogando = 0
        self._etapa_jogadas = False
        self._etapa_aposta = False
        self._etapa_jogadaDealer = False

    def resetRodada(self):
        self._rodada += 1
        self._etapa_jogadas = False
        self._etapa_aposta = False
        self._etapa_jogadaDealer = False
        self.setProximoJogador(0)
        self._dealer.resetCartas()
        for jogadores in self._jogadores:
            jogadores.setDesistencia(False)
            jogadores.resetCartas()

    def getCartasDealer(self):
        return self._dealer.getMao()

    def setBaralho(self, baralho):
        self._baralho = baralho

    def getJogadores(self):
        return self._jogadores

    def setJogadores(self, jogadores):
        self._jogadores = jogadores

    def getJogadorByPosition(self, position):
        for jogador in self._jogadores:
            if jogador.getPosition() == position:
                return jogador

    def setProximoJogador(self, jogador_jogando = -1):
        if jogador_jogando >= 0:
            self._jogador_jogando = jogador_jogando
        else:
            self._jogador_jogando = (self._jogador_jogando+1)%3

    def getJogadorJogando(self):
        return self._jogador_jogando

    def getJogadaDealer(self):
        return self._etapa_jogadaDealer

    def setJogadaDealer(self, jogada_dealer):
        self._etapa_jogadaDealer = jogada_dealer

    def hit(self, position, local = 0):
        jogador = self.getJogadorByPosition(position)
        self.receber_carta_jogador(jogador)

        valorMao = jogador.verificarMao()
        if valorMao < 21:
            resultado = self.criaNotificacao('HIT', local, 'não estourou', position)
        else:
            if valorMao == 21:
                resultado = self.criaNotificacao('HIT', local, 'blackjack', position)
            elif valorMao > 21:
                resultado = self.criaNotificacao('HIT', local, 'perdeu', position)
            if position == 2: # ultimo jogador
                self.setJogadaDealer(True)
            self.setProximoJogador()
        return resultado

    def double(self, position, local = 0):
        jogador = self.getJogadorByPosition(position)
        fichas = jogador.getAposta()
        jogador.dobrarAposta()
        jogador.retirar_fichas(fichas)
        self.receber_carta_jogador(jogador)
        valorMao = jogador.verificarMao()
        resultado = ''
        if valorMao < 21:
            resultado = self.criaNotificacao('DOUBLE', local, 'não estourou', position)
        elif valorMao > 21:
            resultado = self.criaNotificacao('DOUBLE', local, 'perdeu', position)
        elif valorMao == 21:
            resultado = self.criaNotificacao('DOUBLE', local, 'blackjack', position)
        if position == 2: # ultimo jogador
            self.setJogadaDealer(True)
        self.setProximoJogador()
        return resultado

    def stand(self, position, local = 0):
        jogador = self.getJogadorByPosition(position)
        if position == 2: # ultimo jogador
            self.setJogadaDealer(True)
        self.setProximoJogador()
        return self.criaNotificacao('STAND', local, 'parou', position)

    def surrender(self, position, local = 0):
        jogador = self.getJogadorByPosition(position)
        jogador.devolver_metade_aposta()
        jogador.setDesistencia()
        if position == 2: # ultimo jogador
            self.setJogadaDealer(True)
        self.setProximoJogador()
        return self.criaNotificacao('SURRENDER', local, 'desistiu', position)

    def iniciar_partida(self):
        self.distribuir_cartas()
        self._etapa_aposta = True

    def getTurnoAposta(self):
        return self._etapa_aposta

    def getTurnoJogador(self):
        return self._etapa_jogadas

    def verificar_turno(self, jogador):
        return (jogador == self._jogador_jogando)

    def avaliar_aposta(self, fichas, position):
        jogador = self.getJogadorByPosition(position)
        if jogador.avaliarAposta(fichas):
            if position == 2: # ultimo jogador
                self.fimTurnoAposta()
            return "Aposta feita com sucesso"
        else:
            return "Fichas Insuficientes"

    def fimTurnoAposta(self):
        self._etapa_aposta = False
        self._etapa_jogadas = True

    def fimTurnoJogadas(self):
        self._etapa_jogadas = False

    def receive_vitoria(self, position):
        jogador = self.getJogadorByPosition(position)
        jogador.vitoria()
        return f"Você ganhou! :)"

    def receive_empate(self, position):
        jogador = self.getJogadorByPosition(position)
        jogador.empate()
        return f"Você empatou!"

    def receive_derrota(self, position): # Define aposta como 0 para inicio da próxima rodada
        jogador = self.getJogadorByPosition(position)
        jogador.setAposta(0)
        return f"Você perdeu! :("

    def receive_desistencia(self): # Não faz nada, pois o saldo ja foi calculado
        return f"Você desistiu!"

    def receber_carta_jogador(self, jogador):
        carta = self._baralho.retirar_carta()
        jogador.adicionarCarta(carta)

    def receber_carta_dealer(self):
        carta = self._baralho.retirar_carta()
        self._dealer.adicionarCarta(carta)

    def distribuir_cartas(self):
        for numero_cartas in range(2):
            for jogador in self._jogadores:
                self.receber_carta_jogador(jogador)
            self.receber_carta_dealer()
    
    def jogadaDealer(self):
        jogadas = []
        valorD = self._dealer.verificarMao()
        while valorD <= 17:
            self.receber_carta_dealer()
            valorD = self._dealer.verificarMao()

        #comparar mao do dealer com a de todos
        for j in range(len(self._jogadores)):
            jogador = self.getJogadorByPosition(j)
            valorJ = jogador.verificarMao()

            if jogador.getDesistencia():
                resultado = 'desistencia'
            elif (valorJ > valorD and valorJ <= 21) or (valorD > 21 and valorJ <= 21):
                resultado = 'vitoria'
            elif valorJ == valorD and valorJ <= 21:
                resultado = 'empate'
            else:
                resultado = 'derrota'

            jogadas.append({
                'jogada': resultado,
                'jogador': jogador.getPosition()
            })

        self.setJogadaDealer(False)
        return jogadas
