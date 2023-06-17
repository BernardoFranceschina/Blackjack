class Mao():
    def __init__(self,  cartas: list):
        self._cartas = cartas

    def getValor(self):
        valor = 0
        for carta in self._cartas:
            valor += carta.valor
        return valor
    