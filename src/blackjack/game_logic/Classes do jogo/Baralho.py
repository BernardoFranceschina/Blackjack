import random

# lista Naípes e "Números" das cartas
decksuits = ['♠', '♥', '♦', '♣']
deckvalue = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

class Baralho:

    def __init__(self, deck: list):
        # lista com todo baralho
        self.deck = deck

    def createdeck(self):
        for i in range(len(deckvalue)):
            for j in range(len(decksuits)):
                self.deck.append([deckvalue[i], decksuits[j]])
        return self.deck

    def shuffledeck(self):
        return random.shuffle(self.deck)

    #Metodo parecido deve aparece na classe jogo 
    '''def dealcards(self):
        self.hand = []
        for i in range(self.jogadores):
            self.hand.append([])
        for i in range(2):
            for j in range(self.jogadores):
                if i == 0:
                    self.hand[j].extend(self.deck[j])
                else:
                    self.hand[j].append(self.deck[self.jogadores + j][0])
                    self.hand[j].append(self.deck[self.jogadores + j][1]'''

baralho = Baralho([])
print(f"create: \n {baralho.createdeck()}")
baralho.shuffledeck()
print(f"suffle: \n {baralho.deck}")

