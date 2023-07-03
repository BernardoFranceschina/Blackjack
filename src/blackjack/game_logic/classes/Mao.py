class Mao():
    def __init__(self):
        self._cartas = []

    def getCartas(self):
        return [carta.getCarta() for carta in self._cartas]

    def resetCartas(self):
        self._cartas = []

    def adicionaCarta(self, carta):
        self._cartas.append(carta)

    def getValor(self):
        valor = 0
        for carta in self._cartas:
            valor_carta = carta.getValor()
            if valor_carta == 'A':
                if (valor+11) > 21:
                    valor += 1
                else:
                    valor += 11
            else:
                valor += int(valor_carta)
        return valor
    