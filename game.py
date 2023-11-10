from deck import Deck
from player import Player

class Game:

    def __init__(self):
        self.players = [Player("Jugador 1"), Player("Jugador 2")]
        self.deck = Deck()

    def start_hand(self):
        for player in self.players:
            for _ in range(3):  
                card = self.deck.remove_card_deck()  
                player.add_card(card)
        print("Cartas Repartidas")
                

    def table(self):
        turn = 0
        player1_rounds = 0
        player2_rounds = 0
        player1_card_played = None
        player2_card_played = None
        for _ in range (3):
            if player1_rounds!=2 or player2_rounds!=2:
                for _ in range(2):
                        if turn==0:
                            player1_card_played = self.play_round(turn)
                            player1_card_played
                            turn = 1
                        elif turn==1:
                            player2_card_played = self.play_round(turn)
                            player2_card_played
                            turn = 0          
                if player1_card_played.rank > player2_card_played.rank:
                    print(f"La carta {player1_card_played} del Jugador 1 es mayor que {player2_card_played} de Jugador 2")
                else:
                     print(f"La carta {player1_card_played} del Jugador 1 es menor que {player2_card_played} de Jugador 2")
        

    
             

    def play_round(self, pl):
            posicion = int(input("Ingresa la posicion de la carta a jugar: "))
            aux_card_played = self.players[pl].hand[posicion]
            self.players[pl].play_card(posicion)
            return aux_card_played
    
    

    def is_round_over(self):
        test = 1

    # Ganar mano - 1 punto

    # Puntaje truco:
    # Quiero:
    # Truco - 2 puntos
    # Retruco - 3 puntos
    # Vale cuatro - 4 puntos
    # No quiero:
    # Truco - 1 punto
    # Retruco - 2 puntos
    # Vale cuatro - 3 puntos
    
    # Puntaje envido:
    # Quiero:
    # Envido - 2 puntos
    # No quiero:
    # Envido - 1 punto              

    
        
    def is_game_over(self):
        return any(player.points >= 30 for player in self.players)
    
    




