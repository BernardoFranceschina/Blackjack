import os
from tkinter import *
#from tkinter import simpledialog

from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener

class PlayerInterface(PyNetgamesServerListener):
	def __init__(self):
		self.mainWindow = Tk()
		self.mainWindow.title("Blackjack")
		self.mainWindow.geometry("1400x800")
		self.mainWindow.resizable(False, False)
		self.mainWindow["bg"]="green"

		self.frame_cartas_dealer = Frame(self.mainWindow, bg="green", width=1400, height=800)
		self.frame_cartas_j1 = Frame(self.mainWindow, bg="green", width=1400, height=800)

		# Carrega imagens
		self.back = PhotoImage(file=os.path.join(os.path.dirname(__file__), "images/cards/back.png")) #pyimage1
		
		# Label para nome do dealer
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Dealer', font="Arial 17 bold")
		self.dealer_label.place(relx=0.5, rely=0.05, anchor=CENTER)

		self.frame_cartas_dealer.place(relx=0.5, rely=0.15, anchor=CENTER)
		self.frame_cartas_j1.place(relx=0.5, rely=0.73, anchor=CENTER)

		self.viewTier = []
		self.viewTier_j1 = []
		self.add_card_dealer()
		self.add_back_card_dealer()
		self.add_card_j1('1P')

		# Botões das opções dos players
		self.player_hit_button = Button(self.mainWindow, bg="gray", text='Hit', font="Arial 14 bold", command=self.hit)
		self.player_stand_button = Button(self.mainWindow, bg="gray", text='Stand', font="Arial 14 bold", command=self.stand)
		self.player_double_button = Button(self.mainWindow, bg="gray", text='Double', font="Arial 14 bold", command=self.double)
		self.player_surrender_button = Button(self.mainWindow, bg="gray", text='Surrender', font="Arial 14 bold", command=self.surrender)
		self.player_hit_button.place(relx=0.35, rely=0.35, anchor=CENTER, width=140)
		self.player_stand_button.place(relx=0.45, rely=0.35, anchor=CENTER, width=140)
		self.player_double_button.place(relx=0.55, rely=0.35, anchor=CENTER, width=140)
		self.player_surrender_button.place(relx=0.65, rely=0.35, anchor=CENTER, width=140)

		# Label jogador1 e aposta
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Jogador 01', font="Arial 17 bold")
		self.dealer_label.place(relx=0.5, rely=0.60, anchor=CENTER)
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Aposta: 10', font="Arial 12 bold")
		self.dealer_label.place(relx=0.5, rely=0.636, anchor=CENTER)

		self.add_listener()
		self.send_connect()

		self.mainWindow.mainloop()

	def create_card(self, card_name):
		carta = PhotoImage(file=os.path.join(os.path.dirname(__file__), "images/cards/" + card_name + ".png"))
		return carta

	def add_card_j1(self, carta):
		card = self.create_card(carta)
		card_label_j1 = Label(self.frame_cartas_j1, bd=0.1, relief="solid", image=card)
		card_label_j1.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label_j1)

	def add_back_card_dealer(self):
		card_label = Label(self.frame_cartas_dealer, bd=0.1, relief="solid", image=self.back)
		card_label.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label)

	def add_card_dealer(self):
		card_label = Label(self.frame_cartas_dealer, bd=0.1, relief="solid", image=self.back)
		card_label.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label)

	def hit(self):
		self.add_card_j1('1P')

	def stand(self):
		pass

	def double(self):
		self.add_card_j1('1E')

	def surrender(self):
		pass

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

