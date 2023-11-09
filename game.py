from deck import Deck
from card import Card
from player import Player

class Game:

    def __init__(self):
        self.players = [Player("Jugador 1"), Player("Jugador 2")]
        self.deck = Deck()

    def start_game(self):
        for player in self.players:
            for i in range(3):  
                card = self.deck.remove_card_deck()  
                player.add_card(card)

    




