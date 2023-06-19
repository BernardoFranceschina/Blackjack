from .Jogador import *
from .Dealer import *
from .Baralho import *
from .Jogador import *

class Jogo():
    def __init__(self):
        self._baralho = Baralho()
        self._dealer = Dealer()
        self._jogadores = []
        self._etapa_jogadas = False
        self._etapa_aposta = False
        self._rodada = 0
        self._jogador_jogando: 0
        self._etapa_jogadaDealer = False

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

    def hit(self, position):
        jogador = self.getJogadorByPosition(position)
        if jogador.getTurno():
            self.receber_carta_jogador(jogador)

            valorD_mao = jogador.verificarMao()
            if valorD_mao < 21:
                resultado = ""
            else:
                if valorD_mao == 21:
                    resultado = self.notifica_BlackJack()
                elif valorD_mao > 21:
                    resultado = self.notifica_derrota()
                if position == len(self._jogadores) - 1:
                    #self.jogadaDealer()
                    self._etapa_jogadaDealer = True
                jogador.setTurno(False)
            return resultado

    def double(self, position):
        jogador = self.getJogadorByPosition(position)
        if jogador.getTurno():
            fichas = jogador.getAposta()
            fichas_suficientes = jogador.avaliarAposta(fichas)
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
                    #self.jogadaDealer()
                    self._etapa_jogadaDealer = True
                jogador.setTurno(False)
            return notificacao
        else:
            notificacao = ''
            return notificacao

    def stand(self, position):
        jogador = self.getJogadorByPosition(position)
        if jogador.getTurno():
            if position == len(self._jogadores):
                #self.jogadaDealer()
                self._etapa_jogadaDealer = True

    def surrender(self, position):
        jogador = self.getJogadorByPosition(position)
        if jogador.getTurno():
            jogador.devolver_metade_aposta()
            jogador.setJogando_rodada(False)
            if position == len(self._jogadores) - 1:
                #self.jogadaDealer()
                self._etapa_jogadaDealer = True
                notificacao = self.notificar_desistencia
                jogador.setTurno(False)
            return notificacao

    def notifica_BlackJack(self):
        return "Blackjack"

    def notifica_derrota(self):
        return "Derrota"

    def notificar_desistencia():
        return "Desistencia"

    def quantidade_de_jogadores(self):
        return len(self._jogadores)

    def iniciar_partida(self):
        self.distribuir_cartas()
        self._etapa_aposta = True

    def verificar_turno(self, jogador):
        return (jogador == self._jogador_jogando)

    def avaliar_aposta(self, fichas, position): #fichas, jogador(fichas = jogador.fichas? entao apenas jogador?)
        jogador = self.getJogadorByPosition(position)
        if int(fichas) <= int(jogador.getFichas()):
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

    def receive_ganhou(self, position):
        jogador = self.getJogadorByPosition(position)
        jogador.ganhou()
        return f"Jogador {position} - {jogador.getNome()} ganhou do dealer"

    def receive_empatou(self, position):
        jogador = self.getJogadorByPosition(position)
        jogador.empatou()
        return f"Jogador {position} - {jogador.getNome()} empatou contra o dealer"

    def receive_perdeu(self, position):
        jogador = self.getJogadorByPosition(position)
        jogador.perdeu()
        return f"Jogador {position} - {jogador.getNome()} perdeu do dealer"

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
        while valorD > 17:
            self.receber_carta_dealer()
            valorD = self._dealer.verificarMao()

        #comparar mao do dealer com a de todos
        for j in range(len(self._jogadores)- 1):
            jogador = self.getJogadorByPosition(j)
            valorJ = jogador.verificarMao()

            if valorD > valorJ:
                jogada = {'jogada': 'perdeu',
				        'jogador': jogador.getPosition()}
                jogadas.append(jogada)

            elif valorD == valorJ:
                jogada = {'jogada': 'empate',
				        'jogador': jogador.getPosition()}
                jogadas.append(jogada)

            else:
                jogada = {'jogada': 'vitoria',
				        'jogador': jogador.getPosition()}
                jogadas.append(jogada)
        self._etapa_jogadaDealer = False
        return jogadas

