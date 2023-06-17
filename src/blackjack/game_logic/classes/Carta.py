class Carta:
    cartasNumeros = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    cartasNaipes = ['O', 'P', 'C', 'E']

    def __init__(self, numero, naipe):
        self._naipe = naipe
        self._numero = numero

    def getNaipe(self):
        return self._naipe

    def getValor(self):
        if self._numero == 'J':
            return '10'
        if self._numero == 'Q':
            return '10'
        if self._numero == 'K':
            return '10'
        if self._numero == 'A': # Fazer verificação de valor do A
            return '1'
        return self._numero

    def getCarta(self):
        return self._numero + self._naipe