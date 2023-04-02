from tkinter import *

class ActorPlayer:
	def __init__(self):
		self.mainWindow = Tk()
		self.mainWindow.title("Blackjack")
		self.mainWindow.geometry("1400x800")
		self.mainWindow.resizable(False, False)
		self.mainWindow["bg"]="green"

		self.mainFrame = Frame(self.mainWindow, bg="green", width=1400, height=800)
		self.mainFrame_j1 = Frame(self.mainWindow, bg="green", width=1400, height=800)

		# Carrega imagens
		self.back = PhotoImage(file="images/cards/back.png") #pyimage1
		self.heart_1 = PhotoImage(file="images/cards/1_heart.png") #pyimage2

		# Label para nome do dealer
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Dealer', font="Arial 17 bold")
		self.dealer_label.place(relx=0.5, rely=0.05, anchor=CENTER)

		self.mainFrame.place(relx=0.5, rely=0.15, anchor=CENTER)
		self.mainFrame_j1.place(relx=0.5, rely=0.73, anchor=CENTER)

		self.viewTier = []
		self.viewTier_j1 = []
		self.add_card_dealer()
		self.add_back_card_dealer()
		self.add_card_j1()
		self.add_card_j1()

		# Botões das opções dos players
		self.player_hit_label = Button(self.mainWindow, bg="gray", text='Hit', font="Arial 14 bold", command=self.hit)
		self.player_stand_label = Button(self.mainWindow, bg="gray", text='Stand', font="Arial 14 bold", command=self.stand)
		self.player_double_label = Button(self.mainWindow, bg="gray", text='Double', font="Arial 14 bold", command=self.double)
		self.player_surrender_label = Button(self.mainWindow, bg="gray", text='Surrender', font="Arial 14 bold", command=self.surrender)
		self.player_hit_label.place(relx=0.35, rely=0.35, anchor=CENTER, width=140)
		self.player_stand_label.place(relx=0.45, rely=0.35, anchor=CENTER, width=140)
		self.player_double_label.place(relx=0.55, rely=0.35, anchor=CENTER, width=140)
		self.player_surrender_label.place(relx=0.65, rely=0.35, anchor=CENTER, width=140)

		# Label jogador1 e aposta
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Jogador 01', font="Arial 17 bold")
		self.dealer_label.place(relx=0.5, rely=0.60, anchor=CENTER)
		self.dealer_label = Label(self.mainWindow, bg="gray", text='Aposta: 10', font="Arial 12 bold")
		self.dealer_label.place(relx=0.5, rely=0.636, anchor=CENTER)

		self.mainWindow.mainloop()

	def add_card_j1(self):
		card_label_j1 = Label(self.mainFrame_j1, bd=0.1, relief="solid", image=self.heart_1)
		card_label_j1.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label_j1)

	def add_back_card_dealer(self):
		card_label = Label(self.mainFrame, bd=0.1, relief="solid", image=self.back)
		card_label.grid(row=2, column=len(self.viewTier)+1)
		self.viewTier.append(card_label)

	def add_card_dealer(self):
		card_label = Label(self.mainFrame, bd=0.1, relief="solid", image=self.heart_1)
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

ActorPlayer()