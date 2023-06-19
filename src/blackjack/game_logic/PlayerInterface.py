import json
import os
from tkinter import *
from tkinter import simpledialog

from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener

from .classes.Jogador import *
from .classes.Jogo import *

class PlayerInterface(PyNetgamesServerListener):
	def __init__(self):
		# Configuração inicial da tela do jogo
		self.mainWindow = Tk()
		self.mainWindow.title("Blackjack")
		self.mainWindow.geometry("1400x800")
		self.mainWindow.resizable(False, False)
		self.mainWindow["bg"]="green"

		# Cria as instancias dos frames
		self.frames_jogadores = [Frame(self.mainWindow, bg='green',  width=349, height=200) for i in range(3)]
		self.frame_cartas_dealer = Frame(self.mainWindow, bg='green', width=400, height=300)

		# self.player_name = self.dialog_string("Insira seu nome")
		self.player_name = 'sejfqf'

		# Label para nome do dealer
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Dealer', font="Arial 17 bold")
		self.dealer_label.place(relx=0.5, rely=0.05, anchor=CENTER)

		# Posiciona os frames em que ficarão as cartas, tanto dos jogadores quando do dealer
		for index, frame_jogador in enumerate(self.frames_jogadores):
			frame_jogador.place(relx=(index+1)*0.25, rely=0.75, anchor=CENTER)
		self.frame_cartas_dealer.place(relx=0.5, rely=0.15, anchor=CENTER)

		self.grid_dealer = []
		self.grid_jogadores = []
		self.cartas_dealer = []
		self.cartas = []
		self.jogador_label = []
		self.fichas_label = []
		self.aposta_label = []
		self.jogadores = []
		self.jogador = ''
		self.valor_aposta = 0
		self.jogo: Jogo
		self.baralho: Baralho

		# Botões das opções dos players
		self.player_hit_button = Button(self.mainWindow, bg="gray", text='Hit', font="Arial 14 bold", command=self.hit)
		self.player_hit_button.place(relx=0.35, rely=0.35, anchor=CENTER, width=140)
		self.player_stand_button = Button(self.mainWindow, bg="gray", text='Stand', font="Arial 14 bold", command=self.stand)
		self.player_stand_button.place(relx=0.45, rely=0.35, anchor=CENTER, width=140)
		self.player_double_button = Button(self.mainWindow, bg="gray", text='Double', font="Arial 14 bold", command=self.double)
		self.player_double_button.place(relx=0.55, rely=0.35, anchor=CENTER, width=140)
		self.player_surrender_button = Button(self.mainWindow, bg="gray", text='Surrender', font="Arial 14 bold", command=self.surrender)
		self.player_surrender_button.place(relx=0.65, rely=0.35, anchor=CENTER, width=140)

		self.label_notificacao = Label(self.mainWindow, bg="green", text='', font="Arial 17 bold")
		self.label_notificacao.place(relx=0.5, rely=0.45, anchor=CENTER, width=1400)

		self.disable_buttons()
		# self.enable_buttons()

		self.add_listener()
		self.send_connect()

		self.input_aposta = Toplevel()
		self.input_aposta.title('teste')
		self.input_aposta.geometry('300x100')
		self.input_aposta.withdraw()

		Label(self.input_aposta, text="Insira sua aposta - " + self.player_name, font="Arial 12 bold").pack()
		self.teste=Entry(self.input_aposta, width=35)
		self.teste.pack()
		Button(self.input_aposta, text="Apostar", command=lambda: self.aposta()).pack()

		self.mainWindow.mainloop()

	def aposta(self):
		self.input_aposta.withdraw()
		self.valor_aposta = self.teste.get()
		notificacao = self.jogo.avaliar_aposta(self.valor_aposta, self.jogador.getPosition())
		if notificacao == "Aposta feita com sucesso":
			player = self.jogo.getJogadorByPosition(self.jogador.getPosition())
			player.setAposta(self.valor_aposta)
			self.update_player_label(player.getFichas(), player.getAposta(), player.getPosition())
			self.send_move({
				'jogada': 'aposta',
				'jogador': self.jogador.getPosition(),
				'aposta': self.valor_aposta
			})
			self.jogo.setJogadorJogando()
			if self.jogador.getPosition() == len(self.jogo.getJogadores()) - 1:
				self.jogo.fimTurnoAposta()
				self.update_player_hand()
				self.update_dealer_hand()
				self.jogo.setJogadorJogando(0)
				if self.jogador.getPosition() == 0 and self.jogo.getTurnoJogador():
					self.jogador.setTurno()
					self.enable_buttons()
		else:
			self.openAposta()

	def notificacao(self, text):
		self.label_notificacao.config(text=text)

	def dialog_string(self, msg):
		answer = simpledialog.askstring(" ", msg, parent=self.mainWindow)
		return answer

	def dialog_int(self, msg):
		answer = simpledialog.askinteger("", msg, parent=self.mainWindow)
		return answer

	def disable_buttons(self):
		self.player_hit_button.configure(state='disable')
		self.player_stand_button.configure(state='disable')
		self.player_double_button.configure(state='disable')
		self.player_surrender_button.configure(state='disable')

	def enable_buttons(self):
		self.player_hit_button.configure(state='normal')
		self.player_stand_button.configure(state='normal')
		self.player_double_button.configure(state='normal')
		self.player_surrender_button.configure(state='normal')

	def add_player_label(self, jogador, fichas, aposta, numero_jogador):
		self.jogador_label.append(Label(self.mainWindow, bg="gray", text=jogador, font="Arial 17 bold"))
		self.jogador_label[numero_jogador].place(relx=(numero_jogador+1) * 0.25, rely=0.60, anchor=CENTER)
		self.fichas_label.append(Label(self.mainWindow, bg="gray", text='Fichas: ' + str(fichas), font="Arial 12"))
		self.fichas_label[numero_jogador].place(relx=(numero_jogador+1) * 0.25, rely=0.636, anchor=CENTER)
		self.aposta_label.append(Label(self.mainWindow, bg="gray", text='Aposta: ' + str(aposta), font="Arial 12"))
		self.aposta_label[numero_jogador].place(relx=(numero_jogador+1) * 0.25, rely=0.66, anchor=CENTER)

	def update_player_label(self, fichas, aposta, numero_jogador):
		self.fichas_label[numero_jogador].config(text='Fichas: ' + str(fichas))
		self.aposta_label[numero_jogador].config(text='Aposta: ' + str(aposta))

	def update_player_hand(self):
		self.cartas = []
		self.grid_jogadores = []
		for index, jogador in enumerate(self.jogo.getJogadores()):
			for carta in jogador.getMao():
				self.add_card_jogador(index, carta)

	def update_dealer_hand(self):
		self.cartas_dealer = []
		self.grid_dealer = []
		for carta in self.jogo.getCartasDealer():
			self.add_card_dealer(carta)

	def add_card_jogador(self, numero_jogador, carta):
		self.cartas.append(PhotoImage(file=os.path.join(os.path.dirname(__file__), "images/cards/" + carta + ".png")))
		carta = Label(self.frames_jogadores[numero_jogador], bd=0.1, relief="solid", image=self.cartas[len(self.cartas)-1])
		carta.grid(row=0, column=len(self.grid_jogadores)+1)
		self.grid_jogadores.append(carta)

	def add_card_dealer(self, carta):
		self.cartas_dealer.append(PhotoImage(file=os.path.join(os.path.dirname(__file__), "images/cards/" + carta + ".png")))
		carta = Label(self.frame_cartas_dealer, bd=0.1, relief="solid", image=self.cartas_dealer[len(self.cartas_dealer)-1])
		carta.grid(row=0, column=len(self.grid_dealer)+1)
		self.grid_dealer.append(carta)

	def hit(self):
		notificacao = self.jogo.hit(self.jogador.getPosition())
		self.notificacao(notificacao)
		if self.jogador.getPosition() == self.jogo.getJogadorJogando():
			self.enable_buttons()
		else:
			self.disable_buttons()
		
		player = self.jogo.getJogadorByPosition(self.jogador.getPosition())
		self.send_move({
			'jogada': 'hit',
			'jogador': self.jogador.getPosition(),
			'passar_vez': player.getTurno()
		})

	def stand(self):
		notificacao = self.jogo.stand(self.jogador.getPosition())
		self.notificacao(notificacao)
		self.disable_buttons()
		self.send_move({
			'jogada': 'stand',
			'jogador': self.jogador.getPosition(),
			'passar_vez': True
		})

	def double(self):
		notificacao = self.jogo.double(self.jogador.getPosition())
		self.notificacao(notificacao)
		self.disable_buttons()
		self.send_move({
			'jogada': 'double',
			'jogador': self.jogador.getPosition(),
			'passar_vez': True
		})

	def surrender(self):
		notificacao = self.jogo.surrender(self.jogador.getPosition())
		self.notificacao(notificacao)
		self.disable_buttons()
		self.send_move({
			'jogada': 'surrender',
			'jogador': self.jogador.getPosition(),
			'passar_vez': True
		})


	def openAposta(self):
		self.input_aposta.deiconify()

	#----------------------- Pynetgames ----------------------------------

	def add_listener(self):
		self.server_proxy = PyNetgamesServerProxy()
		self.server_proxy.add_listener(self)

	def send_connect(self):
		self.server_proxy.send_connect("wss://py-netgames-server.fly.dev")

	def send_match(self):
		self.server_proxy.send_match(3)

	def receive_connection_success(self):
		print('--------------\nCONETADO')
		self.send_match()

	def receive_disconnect(self):
		print('receive_disconnect')

	def receive_error(self, error):
		print('receive_error', error)

	def receive_match(self, match):
		print('--------------\nPARTIDA INICIADA')

		self.match_id = match.match_id
		self.player_position = match.position
		self.jogo = Jogo()

		# Instancia o jogador local
		self.jogador = Jogador(self.player_name, match.position)
		self.jogadores = []
		self.jogadores.append(self.jogador)

		self.baralho = Baralho()
		if match.position == 0: # Cria e envia o baralho embaralhado para os outros jogadores
			self.create_suffle_and_send_baralho()

		# Envia para os outros jogadores suas informações
		self.send_move({
			'jogada': 'instancia_jogadores',
			'jogador': {
				'nome': self.player_name,
				'position': match.position
			}
		})

	def create_suffle_and_send_baralho(self):
		baralho = Baralho()
		baralho.criar_baralho()
		baralho = baralho.embaralhar()

		move_baralho = []
		for i in baralho:
			move_baralho.append(json.dumps(i.__dict__))

		naipes = [json.loads(i)['_naipe'] for i in move_baralho]
		numeros = [json.loads(i)['_numero'] for i in move_baralho]
		self.baralho.criar_baralho(False, numeros, naipes)
		self.jogo.setBaralho(self.baralho)

		self.send_move({
			'jogada': 'instancia_baralho',
			'baralho': move_baralho
		})

	def send_move(self, payload):
		self.server_proxy.send_move(self.match_id, payload)

	def turno_aposta(self):
		if self.jogo.getTurnoAposta():
			if self.jogo.getJogadorJogando() == self.jogador.getPosition():
				self.openAposta()

	def receive_move(self, message):
		payload = message.payload

		if payload['jogada'] == "instancia_baralho":
			naipes = [json.loads(i)['_naipe'] for i in payload['baralho']]
			numeros = [json.loads(i)['_numero'] for i in payload['baralho']]
			self.baralho.criar_baralho(False, numeros, naipes)
			self.jogo.setBaralho(self.baralho)

		if payload['jogada'] == "instancia_jogadores":
			self.jogadores.append(Jogador(payload['jogador']['nome'], payload['jogador']['position']))
			if len(self.jogadores) == 3:
				self.jogadores = sorted(self.jogadores, key=lambda play: play.getPosition())
				self.jogo.setJogadores(self.jogadores)
				for i, jog in enumerate(self.jogadores):
					self.add_player_label(jog.getNome(), 100, 0, i)
				self.jogo.iniciar_partida()
				self.turno_aposta()

		if payload['jogada'] == "hit":
			notificacao, resultado = self.jogo.receive_hit(payload['jogador'])
			if self.jogador.getPosition() == self.jogo.getJogadorJogando():
				self.enable_buttons()
			else:
				self.disable_buttons()

			self.notificacao(notificacao)
			if resultado == "Blackjack":
				self.notificacao(resultado)
				if self.jogo._etapa_jogadaDealer == True:
					self.jogada_dealer()
			elif resultado == "Derrota":
				self.notificacao(resultado)
				if self.jogo._etapa_jogadaDealer == True:
					self.jogada_dealer()
					self.disable_buttons()

		if payload['jogada'] == "stand":
			notificacao = self.jogo.receive_stand(payload['jogador'])
			if self.jogador.getPosition() == self.jogo.getJogadorJogando():
				self.enable_buttons()
			else:
				self.disable_buttons()
			self.notificacao(notificacao)
			if self.jogo._etapa_jogadaDealer == True:
					self.jogada_dealer()

		if payload['jogada'] == "double":
			notificacao = self.jogo.receive_double(payload['jogador'])
			if self.jogador.getPosition() == self.jogo.getJogadorJogando():
				self.enable_buttons()
			else:
				self.disable_buttons()
			self.notificacao(notificacao)
			if self.jogo._etapa_jogadaDealer == True:
					self.jogada_dealer()

		if payload['jogada'] == "surrender":
			notificacao = self.jogo.receive_surrender(payload['jogador'])
			if self.jogador.getPosition() == self.jogo.getJogadorJogando():
				self.enable_buttons()
			else:
				self.disable_buttons()
			self.notificacao(notificacao)
			if self.jogo._etapa_jogadaDealer == True:
					self.jogada_dealer()

		if payload['jogada'] == "ganhou":
			notificacao = self.jogo.receive_ganhou(payload['jogador'])
			self.notificacao(notificacao)

		if payload['jogada'] == "perdeu":
			notificacao = self.jogo.receive_perdeu(payload['jogador'])
			self.notificacao(notificacao)

		if payload['jogada'] == "aposta":
			position = payload['jogador']
			aposta = payload['aposta']
			jogador = self.jogo.getJogadorByPosition(position)
			jogador.setAposta(aposta)
			for p in self.jogo.getJogadores():
				self.update_player_label(p.getFichas(), p.getAposta(), p.getPosition())

			if position == len(self.jogo.getJogadores()) - 1:
				self.jogo.fimTurnoAposta()
				self.update_player_hand()
				self.update_dealer_hand()
				self.jogo.setJogadorJogando(0)
				if self.jogador.getPosition() == 0 and self.jogo.getTurnoJogador():
					self.jogador.setTurno()
					self.enable_buttons()
		
			if self.jogo.getTurnoAposta():
				self.jogo.setJogadorJogando()
				if self.jogo.getJogadorJogando() == self.jogador.getPosition():
					self.openAposta()

		if payload['jogada'] != "instancia_jogadores" and payload['jogada'] != 'instancia_baralho' and payload['jogada'] != 'aposta':
			self.update_player_hand()
			self.update_dealer_hand()

	def jogada_dealer(self):
		#resultados = lista de dicionarios [{'jogada': perdeu/ganhou/empatou, 'jogador': posicao}]
		resultados = self.jogo.jogadaDealer()
		for dic in resultados:
			self.send_move({
				'jogada': dic['jogada'],
				'jogador': dic['jogador']
			})
