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
            ("3", None): 10,  
            ("2", None): 9,   
            ("1", "copa"): 8,
            ("1", "oro"): 8,
            ("12", None): 7,  
            ("11", None): 6,  
            ("10", None): 5,  
            ("7", "basto"): 4,
            ("7", "copa"): 4,  
            ("6", None): 3,   
            ("5", None): 2,   
            ("4", None): 1    
    }
        return rankings.get((self.valor, self.palo), 0)

    def __repr__(self):
        v = self.VALORES[self.valor] +\
            " de " + \
            self.PALOS[self.palo]
        return v  