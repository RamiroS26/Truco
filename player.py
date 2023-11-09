from card import Card
from deck import Deck

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.points = 0

    def add_card(self, card):
        self.hand.append(card)

    def play_card(self, posicion):
        if 0 <= posicion < len(self.hand):
            carta = self.hand[posicion]
            self.hand.pop(posicion)
            print(f"{self.name} juega la carta: {carta}")
            return carta
        else:
            print(f"{self.name}, la posición {posicion} no es válida.")
            return None
        
    def __repr__(self):
        hand_info = ", ".join(str(card) for card in self.hand)
        return f"{self.name} | Puntos: {self.points} | Cartas en mano: {len(self.hand)} | Cartas: {hand_info}"
    