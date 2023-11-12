from deck import Deck
from player import Player

class Game:

    def __init__(self):
        self.players = [Player("Jugador 1"), Player("Jugador 2")]
        self.deck = Deck()
        self.truco = False
        self.envido = False

    def start_hand(self):           # Crear manos
        for player in self.players:
            for _ in range(3):  
                card = self.deck.remove_card_deck()  
                player.add_card(card)
        print("Cartas Repartidas")
                

    def table(self):    # Mesa del juego           
        turn = 0                                   # Si van pardas la primera baza, gana las dos bazas el que mata en la segunda. 
        player1_rounds = 0                         # Si por casualidad (o a propósito) siguen las dos primeras también pardas, gana el que sienta la tercera baza. 
        player2_rounds = 0                         # Y si fueran pardas las tres, gana el truco el que es mano de los que han empardado la última.
        player1_card_played = None                 # rounds = bazas
        player2_card_played = None
        round = 1
        pardas = False
        player1 = self.players[0]
        player2 = self.players[1]
        for _ in range(3):
            points_round=0
            if player1_rounds!=2 or player2_rounds!=2:
                if round==3 and pardas and player1_rounds==1:       # Verificar pardas. Si P1 pardas primera mano y P1 gana segunda mano, P1 gana la mano
                    points_round+=1
                    if self.truco: points_round+=1                     # Verificar si se jugó un truco
                    print(f"{player1.name} ganó la mano. +{points_round}")
                    player1.points+=points_round                    # Sumar los puntos al chico
                    break                                           # Salir del bucle para empezar otra mano
                elif round==3 and pardas and player2_rounds==1:
                    points_round+=1
                    if self.truco: points_round+=1
                    print(f"{player2.name} ganó la mano. +{points_round}")
                    player2.points+=points_round
                    break        
                for _ in range(2):              # Turnos para jugar las cartas. El P1 siempre es mano. 
                        if turn==0:
                            self.menu(self.truco, self.envido, round, player1.name)   # Invocar el menu
                            player1_card_played = self.play_round(turn)
                            player1_card_played                             # Invocar metodo para jugar carta
                            turn = 1                                        # Cambiar el turno para que juegue el player 2
                        elif turn==1:
                            self.menu(self.truco, self.envido, round, player2.name)
                            player2_card_played = self.play_round(turn)
                            player2_card_played
                            turn = 0          
                if player1_card_played.rank > player2_card_played.rank:       # Comparaciones de cartas
                    player1_rounds+1
                    round+1
                    print(f"La carta del jugador {player1.name} {player1_card_played} es mayor a {player2_card_played}")
                elif player1_card_played.rank < player2_card_played.rank:
                    player2_rounds+1
                    round+1
                    print(f"La carta del jugador {player1.name} {player1_card_played} es mayor a {player2_card_played}")
                else:                                               # Si es empate = pardas
                     pardas = True
                     round+1
                     print("Pardas")
            if player1_rounds==2:                                   # Verificar el ganador de la mano
                points_round+=1
                if self.truco: points_round+=1
                break
            elif player2_rounds==2:
                points_round+=1
                if self.truco: points_round+=1
                break             
    
    def menu(self, truco, envido, round, player):                                  # Truco/Envido = true -> Ya se jugó, no se puede jugar
        num=-1
        while num!=0:
            if (not truco and not envido and round==1):
                    print(f"\tTurno de {player}")
                    print("---------------------------------")
                    print("-Ingrese 1 para cantar envido")
                    print("-Ingrese 2 para cantar truco")
                    print("-Ingrese 0 para continuar")
                    num=int(input("-> "))
                    while num!=0:
                        match num:
                            case 1:
                                self.cantar_envido()
                                num=int(input("-> "))
                            case 2:
                                self.cantar_truco()
                                num=int(input("-> "))
                            case _:
                                int(input("Ingrese el numero correcto -> "))
            elif (truco and not envido and round==1):
                    print(f"\tTurno de {player}")
                    print("---------------------------------")
                    print("-Ingrese 1 para cantar envido")
                    print("-Ingrese 0 para continuar")
                    num=int(input("-> "))
                    while num!=0:
                        if num==1: 
                            self.cantar_envido()
                            num=int(input("-> "))
                        else: int(input("Ingrese el numero correcto -> "))
            elif(not truco):
                    print(f"\tTurno de {player}")
                    print("---------------------------------")
                    print("-Ingrese 1 para cantar truco")
                    print("-Ingrese 0 para continuar")
                    num=int(input("-> "))
                    while num!=0:
                        if num==1: 
                            self.cantar_truco()
                            num=int(input("-> "))
                        else: int(input("Ingrese el numero correcto -> "))
            elif(truco):
                    print(f"\tTurno de {player}")
                    print("---------------------------------")
                    print("-Ingrese 0 para continuar")
                    num=int(input("-> "))
                    while num != 0:
                        int(input("Ingrese el numero correcto -> "))

         
    def cantar_truco(self, player):
        print(f"{player} cantó truco.")
        while True:
            choice = input("Quiero / No quiero (q/nq):").lower()
            if choice == "q" or choice == "nq": break
        if choice == "q": 
             self.truco = True
             print("Truco aceptado")
        else: 
             self.truco = False
             print("Truco no aceptado")

    #def cantar_envido(self, player):
        print(f"{player} cantó envido.")
        while True:
            choice = input("Quiero / No quiero (q/nq):").lower()
            if choice == "q" or choice == "nq": break
        if choice == "q": 
             self.envido = True
             print("Envido aceptado")
        else: 
             self.envido = False
             print("Envido no aceptado")
    
    def calculate_envido(self, hand_p1, hand_p2):
        None
        
    
             

    def play_round(self, pl):
            while True:
                posicion = int(input("Ingresa la posicion de la carta a jugar: "))
                if posicion in range(3):
                    break
            aux_card_played = self.players[pl].hand[posicion]
            self.players[pl].play_card(posicion)
            return aux_card_played
    
    

    def is_round_over(self):
        None

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
    
    




