from deck import Deck
from card import Card
from player import Player
from table import Table

class Game:

    def __init__(self):
        self.players = [Player("Jugador 1"), Player("Jugador 2")]
        self.deck = Deck()
        self.table = Table(self.players)

    def start_hand(self):
        for player in self.players:
            for i in range(3):  
                card = self.deck.remove_card_deck()  
                player.add_card(card)

    def is_over(self):
        return any(player.points >= 30 for player in self.players)
    




