class Card:

    PALOS = ["espada", "basto", "copa", "oro"]
    VALORES = [None, "1", "2", "3", "4", "5", "6", "7", None, None, "10", "11", "12"]

    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo
        self.rank = self.asign_rank()

    def asign_rank(self):
        card_key = (str(self.valor), str(self.palo))
        match card_key:
            case ("1", "0"): return 14
            case ("1", "1"): return 13
            case ("7", "0"): return 12
            case ("7", "3"): return 11
            case ("3", _): return 10
            case ("2", _): return 9
            case ("1", "3"): return 8
            case ("1", "2"): return 8
            case ("12", _): return 7
            case ("11", _): return 6
            case ("10", _): return 5
            case ("6", _): return 3
            case ("5", _): return 2
            case ("4", _): return 1
            case ("7", "2"): return 4
            case ("7", "1"): return 4
            case _: return 0
        
    
    def __gt__(self, c2):
        return self.rank > c2.rank
    
    def __lt__(self, c2):
        return self.rank < c2.rank
    
    def __eq__(self, c2):
        return self.rank == c2.rank

    def __repr__(self):
        v = self.VALORES[self.valor] +\
            " de " + \
            self.PALOS[self.palo]
        return v  