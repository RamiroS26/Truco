from card import Card
from random import shuffle

class Deck:

    def __init__(self):
        self.cards = []
        for numero in range(1,13):
            for palo in range(4):
                if numero not in ["8","9"]:
                    self.cards.append(Card(numero,palo))
