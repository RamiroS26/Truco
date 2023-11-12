from card import Card
from random import shuffle

class Deck:

    def __init__(self):
        self.cards = []
        for numero in range(1,13):          # Crear mazo
            for palo in range(4):
                if numero not in [8,9]:
                    self.cards.append(Card(numero,palo))
        shuffle(self.cards)

    def remove_card_deck(self):          # Remover una carta del mazo
        if len(self.cards) == 0:
            return "Deck Empty"
        return self.cards.pop()
    
    def shuffle_deck(self):         # Mezclar mazo
        shuffle(self.cards)
    
    def get_remaining_cards(self):
        return len(self.cards)

    def print_deck(self):       # Debugging
        for card in self.cards:
            print(card.rank)