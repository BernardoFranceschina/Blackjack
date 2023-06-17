import os
from tkinter import *

from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener

class PlayerInterface(PyNetgamesServerListener):
	def __init__(self):
		self.mainWindow = Tk()
		self.mainWindow.title("Blackjack")
		self.mainWindow.geometry("1400x800")
		self.mainWindow.resizable(False, False)
		self.mainWindow["bg"]="green"

		self.frames_jogadores = [Frame(self.mainWindow, width=349, height=200) for i in range(4)]
		self.frame_cartas_dealer = Frame(self.mainWindow, width=1400, height=800)
		
		# Carrega imagens
		self.back = PhotoImage(file=os.path.join(os.path.dirname(__file__), "images/cards/back.png")) #pyimage1
		self.heart_1 = PhotoImage(file=os.path.join(os.path.dirname(__file__), "images/cards/1P.png")) #pyimage2
		
		# Label para nome do dealer
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Dealer', font="Arial 17 bold")
		self.dealer_label.place(relx=0.5, rely=0.05, anchor=CENTER)

		for index, frame_jogador in enumerate(self.frames_jogadores):
			frame_jogador.place(relx=(index+1)*0.2, rely=0.75, anchor=CENTER)

		self.grid_dealer = []
		self.grid_jogadores = []

		self.add_card_dealer()

		self.add_card_jogador(0)
		self.add_card_jogador(1)
		self.add_card_jogador(2)
		self.add_card_jogador(3)
		
		# Botões das opções dos players
		self.player_hit_button = Button(self.mainWindow, bg="gray", text='Hit', font="Arial 14 bold", command=self.hit)
		self.player_hit_button.place(relx=0.35, rely=0.35, anchor=CENTER, width=140)
		self.player_stand_button = Button(self.mainWindow, bg="gray", text='Stand', font="Arial 14 bold", command=self.stand)
		self.player_stand_button.place(relx=0.45, rely=0.35, anchor=CENTER, width=140)
		self.player_double_button = Button(self.mainWindow, bg="gray", text='Double', font="Arial 14 bold", command=self.double)
		self.player_double_button.place(relx=0.55, rely=0.35, anchor=CENTER, width=140)
		self.player_surrender_button = Button(self.mainWindow, bg="gray", text='Surrender', font="Arial 14 bold", command=self.surrender)
		self.player_surrender_button.place(relx=0.65, rely=0.35, anchor=CENTER, width=140)
		#FIM Botões das opções dos players

		self.add_player_label('Jogador 01', 100, 10, 0)
		self.add_player_label('Jogador 02', 100, 10, 1)
		self.add_player_label('Jogador 03', 100, 10, 2)
		self.add_player_label('Jogador 04', 100, 10, 3)
		
		# self.disable_buttons()
		# self.enable_buttons()

		self.add_listener()
		self.send_connect()

		self.mainWindow.mainloop()

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

	def add_card_jogador(self, numero_jogador):
		carta = Label(self.frames_jogadores[numero_jogador], bd=0.1, relief="solid", image=self.heart_1)
		carta.grid(row=0, column=len(self.grid_jogadores)+1)
		self.grid_jogadores.append(carta)

	def add_card_dealer(self):
		carta = Label(self.frame_cartas_dealer, bd=0.1, relief="solid", image=self.heart_1)
		carta.grid(row=0, column=len(self.grid_dealer)+1)
		self.grid_dealer.append(carta)

	def hit(self):
		self.add_card_dealer()

	def stand(self):
		self.add_card_jogador(1)

	def double(self):
		self.add_card_jogador(2)

	def surrender(self):
		self.add_card_jogador(3)

	#----------------------- Pynetgames ----------------------------------

	def add_listener(self):
		self.server_proxy = PyNetgamesServerProxy()
		self.server_proxy.add_listener(self)

	def send_connect(self):
		self.server_proxy.send_connect("wss://py-netgames-server.fly.dev")

	def send_match(self):
		self.server_proxy.send_match(2)

	def receive_connection_success(self):
		print('--------------\nCONETADO ')
		self.send_match()

	def receive_disconnect(self):
		pass
		
	def receive_error(self, error):
		pass

	def receive_match(self, match):
		print('--------------\nPARTIDA INICIADA')
		print('--------------\nORDEM: ', match.position)
		print('--------------\nmatch_id: ', match.match_id)
		print('--------------')

	def receive_move(self, move):
		pass


class DynamicGrid(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, *args, **kwargs)
		self.text = Text(self, wrap="char", borderwidth=0, highlightthickness=0,
						    state="disabled")
		self.text.pack(fill="both", expand=True)
		self.boxes = []

	def add_box(self):
		bg = "red"
		box = Frame(self.text, bd=1, relief="sunken", background=bg,
				       width=100, height=100)
		self.boxes.append(box)
		self.text.configure(state="normal")
		self.text.window_create("end", window=box)
		self.text.configure(state="disabled")

