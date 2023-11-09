
class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.points = 0

    def add_card(self, card):
        self.hand.append(card)
        
    def __repr__(self):
        hand_info = ", ".join(str(card) for card in self.hand)
        return f"{self.name} | Puntos: {self.points} | Cartas en mano: {len(self.hand)} | Cartas: {hand_info}"
        