from player import Player

class Table:
    def __init__(self, players):
        self.players = players
        self.hands_played = 0 
        self.team_points = [0, 0]
        
    def play_hand(self, num):
        cards_played = Player[0].play_card(1) 