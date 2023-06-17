class Mao():
    def __init__(self, cartas):
        self._cartas = cartas

    def adicionaCarta(self, carta):
        self._cartas.append(carta)

    def getValor(self):
        valor = 0
        for carta in self._cartas:
            valor += int(carta.getValor())
        return valor
    