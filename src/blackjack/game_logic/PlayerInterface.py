import os
from tkinter import *
from tkinter import simpledialog

from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener

class PlayerInterface(PyNetgamesServerListener):
	def __init__(self):
		# Configuração inicial da tela do jogo
		self.mainWindow = Tk()
		self.mainWindow.title("Blackjack")
		self.mainWindow.geometry("1400x800")
		self.mainWindow.resizable(False, False)
		self.mainWindow["bg"]="green"

		# Cria as instancias dos frames
		self.frames_jogadores = [Frame(self.mainWindow, width=349, height=200) for i in range(4)]
		self.frame_cartas_dealer = Frame(self.mainWindow, width=400, height=800)

		self.player_name = self.dialog_string("Insira seu nome")
		# Label para nome do dealer
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Dealer', font="Arial 17 bold")
		self.dealer_label.place(relx=0.5, rely=0.05, anchor=CENTER)

		# Posiciona os frames em que ficarão as cartas, tanto dos jogadores quando do dealer
		for index, frame_jogador in enumerate(self.frames_jogadores):
			frame_jogador.place(relx=(index+1)*0.2, rely=0.75, anchor=CENTER)
		self.frame_cartas_dealer.place(relx=0.5, rely=0.15, anchor=CENTER)

		self.grid_dealer = []
		self.grid_jogadores = []
		self.cartas_dealer = []
		self.cartas = []
		
		self.add_card_dealer('back')
		self.add_card_jogador(0, '1P')
		self.add_card_jogador(1, '1E')
		self.add_card_jogador(2, '1O')
		self.add_card_jogador(3, '1C')

		# Botões das opções dos players
		self.player_hit_button = Button(self.mainWindow, bg="gray", text='Hit', font="Arial 14 bold", command=self.hit)
		self.player_hit_button.place(relx=0.35, rely=0.35, anchor=CENTER, width=140)
		self.player_stand_button = Button(self.mainWindow, bg="gray", text='Stand', font="Arial 14 bold", command=self.stand)
		self.player_stand_button.place(relx=0.45, rely=0.35, anchor=CENTER, width=140)
		self.player_double_button = Button(self.mainWindow, bg="gray", text='Double', font="Arial 14 bold", command=self.double)
		self.player_double_button.place(relx=0.55, rely=0.35, anchor=CENTER, width=140)
		self.player_surrender_button = Button(self.mainWindow, bg="gray", text='Surrender', font="Arial 14 bold", command=self.surrender)
		self.player_surrender_button.place(relx=0.65, rely=0.35, anchor=CENTER, width=140)

		self.add_player_label('Jogador 01', 100, 10, 0)
		self.add_player_label('Jogador 02', 100, 10, 1)
		self.add_player_label('Jogador 03', 100, 10, 2)
		self.add_player_label('Jogador 04', 100, 10, 3)

		# self.disable_buttons()
		# self.enable_buttons()

		self.add_listener()
		self.send_connect()

		menubar = Menu(self.mainWindow) 
		file = Menu(menubar, tearoff = 0) 
		menubar.add_cascade(label ='Jogo', menu = file) 
		file.add_command(label ='Iniciar Jogo', command=lambda: self.send_match())
		
		self.mainWindow.config(menu = menubar) 

		self.mainWindow.mainloop()

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
		jogador_label = Label(self.mainWindow, bg="gray", text=jogador, font="Arial 17 bold")
		jogador_label.place(relx=(numero_jogador+1) * 0.2, rely=0.60, anchor=CENTER)
		fichas_label = Label(self.mainWindow, bg="gray", text='Fichas: ' + str(fichas), font="Arial 12")
		fichas_label.place(relx=(numero_jogador+1) * 0.2, rely=0.636, anchor=CENTER)
		aposta_label = Label(self.mainWindow, bg="gray", text='Aposta: ' + str(aposta), font="Arial 12")
		aposta_label.place(relx=(numero_jogador+1) * 0.2, rely=0.66, anchor=CENTER)

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
		self.add_card_jogador(0, '1C')

	def stand(self):
		self.add_card_jogador(1, '1C')

	def double(self):
		self.add_card_jogador(2, '1C')

	def surrender(self):
		self.add_card_jogador(3, '1C')

	#----------------------- Pynetgames ----------------------------------

	def add_listener(self):
		self.server_proxy = PyNetgamesServerProxy()
		self.server_proxy.add_listener(self)

	def send_connect(self):
		self.server_proxy.send_connect("wss://py-netgames-server.fly.dev")

	def send_match(self):
		self.server_proxy.send_match(2)

	def receive_connection_success(self):
		print('--------------\nCONETADO')

	def receive_disconnect(self):
		print('receive_disconnect', self)
		
	def receive_error(self, error):
		print('receive_error', error)

	def receive_match(self, match):
		print('--------------\nPARTIDA INICIADA')
		print('--------------\nORDEM: ', match.position)
		print('--------------\nmatch_id: ', match.match_id)
		print('--------------')
		self.dialog_int("Aposta")

	def receive_move(self, move):
		print('receive_move', move)
