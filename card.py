class Card:

    PALOS = ["espada", "basto", "copa", "oro"]
    VALORES = [None, "1", "2", "3", "4", "5", "6", "7", None, None, "10", "11", "12"]

    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo
        self.rank = self.asign_rank()

    def asign_rank(self):
        rankings = {
            ("1", "espada"): 14,
            ("1", "basto"): 13,
            ("7", "espada"): 12,
            ("7", "oro"): 11,  
            ("1", "copa"): 8,
            ("1", "oro"): 8,
            ("7", "basto"): 4,
            ("7", "copa"): 4,   
    }
        if str(self.valor) == "3":
            return 10
        elif str(self.valor) == "2":
            return 9
        elif str(self.valor) == "12":
            return 7
        elif str(self.valor) == "11":
            return 6
        elif str(self.valor) == "10":
            return 5
        elif str(self.valor) == "6":
            return 3
        elif str(self.valor) == "5":
            return 2
        elif str(self.valor) == "4":
            return 1

        return rankings.get((self.valor, self.palo), 0)

    def __repr__(self):
        v = self.VALORES[self.valor] +\
            " de " + \
            self.PALOS[self.palo]
        return v  