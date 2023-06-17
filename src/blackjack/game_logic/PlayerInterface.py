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
		self.frame_cartas_j1 = Frame(self.mainWindow, bg="green", width=349, height=200)
		self.frame_cartas_j2 = Frame(self.mainWindow, bg="green", width=349, height=200)
		self.frame_cartas_j3 = Frame(self.mainWindow, bg="green", width=349, height=200)
		self.frame_cartas_j4 = Frame(self.mainWindow, bg="green", width=349, height=200)

		# Carrega imagens )
		self.back = PhotoImage(file=os.path.join(os.path.dirname(__file__), "images/cards/back.png")) #pyimage1
		self.heart_1 = PhotoImage(file=os.path.join(os.path.dirname(__file__), "images/cards/1P.png")) #pyimage2
		
		# Label para nome do dealer
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Dealer', font="Arial 17 bold")
		self.dealer_label.place(relx=0.5, rely=0.05, anchor=CENTER)

		self.frame_cartas_dealer.place(relx=0.5, rely=0.15, anchor=CENTER)
		self.frame_cartas_j1.place(relx=0.2, rely=0.75, anchor=CENTER)
		self.frame_cartas_j2.place(relx=0.4, rely=0.75, anchor=CENTER)
		self.frame_cartas_j3.place(relx=0.6, rely=0.75, anchor=CENTER)
		self.frame_cartas_j4.place(relx=0.8, rely=0.75, anchor=CENTER)

		self.viewTier = []
		self.add_card_dealer()
		self.add_card_j1()
		self.add_card_j2()
		self.add_card_j2()
		self.add_card_j3()
		self.add_card_j4()
		self.add_card_j4()
		self.add_card_j4()

		# Botões das opções dos players
		self.player_hit_button = Button(self.mainWindow, bg="gray", text='Hit', font="Arial 14 bold", command=self.hit)
		self.player_hit_button.place(relx=0.35, rely=0.35, anchor=CENTER, width=140)

		self.player_stand_button = Button(self.mainWindow, bg="gray", text='Stand', font="Arial 14 bold", command=self.stand)
		self.player_stand_button.place(relx=0.45, rely=0.35, anchor=CENTER, width=140)

		self.player_double_button = Button(self.mainWindow, bg="gray", text='Double', font="Arial 14 bold", command=self.double)
		self.player_double_button.place(relx=0.55, rely=0.35, anchor=CENTER, width=140)

		self.player_surrender_button = Button(self.mainWindow, bg="gray", text='Surrender', font="Arial 14 bold", command=self.surrender)
		self.player_surrender_button.place(relx=0.65, rely=0.35, anchor=CENTER, width=140)

		self.add_player_label('Jogador 02', 100, 10, 1)
		self.add_player_label('Jogador 01', 100, 10, 0)
		self.add_player_label('Jogador 03', 100, 10, 2)
		self.add_player_label('Jogador 04', 100, 10, 3)

		# self.add_listener()
		# self.send_connect()

		self.mainWindow.mainloop()

	def add_player_label(self, jogador, fichas, aposta, numero_jogador):
		jogador_label = Label(self.mainWindow, bg="gray", text=jogador, font="Arial 17 bold")
		jogador_label.place(relx=(numero_jogador+1) * 0.2, rely=0.60, anchor=CENTER)
		fichas_label = Label(self.mainWindow, bg="gray", text='Fichas: ' + str(fichas), font="Arial 12")
		fichas_label.place(relx=(numero_jogador+1) * 0.2, rely=0.636, anchor=CENTER)
		aposta_label = Label(self.mainWindow, bg="gray", text='Aposta: ' + str(aposta), font="Arial 12")
		aposta_label.place(relx=(numero_jogador+1) * 0.2, rely=0.66, anchor=CENTER)

	def add_card_j1(self):
		card_label_j1 = Label(self.frame_cartas_j1, bd=0.1, relief="solid", image=self.heart_1)
		card_label_j1.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label_j1)

	def add_card_j2(self):
		card_label_j2 = Label(self.frame_cartas_j2, bd=0.1, relief="solid", image=self.heart_1)
		card_label_j2.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label_j2)

	def add_card_j3(self):
		card_label_j3 = Label(self.frame_cartas_j3, bd=0.1, relief="solid", image=self.heart_1)
		card_label_j3.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label_j3)

	def add_card_j4(self):
		card_label_j4 = Label(self.frame_cartas_j4, bd=0.1, relief="solid", image=self.heart_1)
		card_label_j4.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label_j4)

	def add_card_dealer(self):
		card_label = Label(self.frame_cartas_dealer, bd=0.1, relief="solid", image=self.back)
		card_label.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label)

	def hit(self):
		self.add_card_j1()

	def stand(self):
		pass

	def double(self):
		self.add_card_j1()

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

