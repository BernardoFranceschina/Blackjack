from .Jogador import *
from .Dealer import *
from .Baralho import *
from .Jogador import *

class Jogo():
    def __init__(self):
        self._baralho = Baralho()
        self._dealer = Dealer()
        self._jogadores = []
        self._rodada = 0
        self._jogador_jogando = 0
        self._etapa_jogadas = False
        self._etapa_aposta = False
        self._etapa_jogadaDealer = False

    def resetRodada(self):
        self._etapa_jogadas = False
        self._etapa_aposta = False
        self._etapa_jogadaDealer = False
        self.setJogadorJogando(0)
        self._dealer.resetCartas()
        for jogadores in self._jogadores:
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

    def setJogadorJogando(self, jogador_jogando = -1):
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

    def hit(self, position):
        jogador = self.getJogadorByPosition(position)
        self.receber_carta_jogador(jogador)

        valorD_mao = jogador.verificarMao()
        if valorD_mao < 21:
            resultado = " "
        else:
            if valorD_mao == 21:
                resultado = self.notifica_BlackJack()
            elif valorD_mao > 21:
                resultado = self.notifica_derrota()
            if position == len(self._jogadores) - 1:
                self.setJogadaDealer(True)
            jogador.setTurno(False)
            self.setJogadorJogando()
            return resultado
        

    def double(self, position):
        jogador = self.getJogadorByPosition(position)
        fichas = jogador.getAposta()
        fichas_suficientes = jogador.avaliarAposta(fichas)
        notificacao = ''
        if fichas_suficientes:
            jogador.dobrarAposta()
            jogador.retirar_fichas(fichas)
            self.receber_carta_jogador(jogador)
            valorDM = jogador.verificarMao()
            if valorDM > 21:
                notificacao = self.notifica_derrota()
            elif valorDM == 21:
                notificacao = self.notifica_BlackJack()
            if position == len(self._jogadores) - 1:
                self.setJogadaDealer(True)
            jogador.setTurno(False)
            self.setJogadorJogando()
        return notificacao

    def stand(self, position):
        jogador = self.getJogadorByPosition(position)
        jogador.setTurno(False)
        if position == len(self._jogadores) - 1:
            self.setJogadaDealer(True)
        self.setJogadorJogando()

    def surrender(self, position):
        jogador = self.getJogadorByPosition(position)
        jogador.setTurno(False)
        jogador.devolver_metade_aposta()
        if position == len(self._jogadores) - 1:
            self.setJogadaDealer(True)
        self.setJogadorJogando()
        return self.notificar_desistencia()

    def notifica_BlackJack(self):
        return "Blackjack"

    def notifica_derrota(self):
        return "Derrota"

    def notificar_desistencia(self):
        return "Desistencia"

    def quantidade_de_jogadores(self):
        return len(self._jogadores)

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
            if position == len(self._jogadores) - 1:
                self.fimTurnoAposta()
            return "Aposta feita com sucesso"
        else:
            return "Fichas Insuficientes"

    def fimTurnoAposta(self):
        self._etapa_aposta = False
        self._etapa_jogadas = True

    def fimTurnoJogadas(self):
        self._etapa_jogadas = False

    def receive_hit(self, position):
        jogador = self.getJogadorByPosition(position)
        resultado = self.hit(position)
        notificacao = f"Jogador {position} - {jogador.getNome()} pegou mais uma carta: HIT\n"
        return notificacao, resultado
        #return f"Jogador {position} - {jogador.getNome()} pegou mais uma carta: HIT\n{notificacao}"

    def receive_double(self, position):
        jogador = self.getJogadorByPosition(position)
        notificacao = self.double(position)
        return f"Jogador {position} - {jogador.getNome()} dobrou aposta e pegou mais uma carta: DOUBLE\n{notificacao}"

    def receive_stand(self, position):
        jogador = self.getJogadorByPosition(position)
        notificacao = self.stand(position)
        return f"Jogador {position} - {jogador.getNome()} passou a vez: STAND\n{notificacao}"

    def receive_surrender(self, position):
        jogador = self.getJogadorByPosition(position)
        notificacao = self.surrender(position)
        return f"Jogador {position} - {jogador.getNome()} se rendeu. Metade das fichas foram devolvidas: SURRENDER\n{notificacao}"

    def receive_vitoria(self, position):
        jogador = self.getJogadorByPosition(position)
        jogador.vitoria()
        return f"Você ganhou! :)"
        return f"Jogador {position} - {jogador.getNome()} ganhou do dealer/voce"

    def receive_empate(self, position):
        jogador = self.getJogadorByPosition(position)
        jogador.empate()
        return f"Você empatou!"
        return f"Jogador {position} - {jogador.getNome()} empatou contra o dealer/voce"

    def receive_derrota(self, position):
        jogador = self.getJogadorByPosition(position)
        return f"Você perdeu! :("
        return f"Jogador {position} - {jogador.getNome()} perdeu/voce"

    def notificacao_derrota(self, position):
        jogador = self.getJogadorByPosition(position)
        return f"Jogador {position} - {jogador.getNome()} perdeu"

    def notificacao_blackjack(self, position):
        jogador = self.getJogadorByPosition(position)
        return f"Jogador {position} - {jogador.getNome()} fez um BlackJack"

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
        while valorD < 17:
            self.receber_carta_dealer()
            valorD = self._dealer.verificarMao()

        #comparar mao do dealer com a de todos
        for j in range(len(self._jogadores)):
            jogador = self.getJogadorByPosition(j)
            valorJ = jogador.verificarMao()

            if (valorJ > valorD and valorJ <= 21) or (valorD > 21 and valorJ <= 21):
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
