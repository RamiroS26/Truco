from random import shuffle
import discord
from discord.ext import commands

class Card:

    PALOS = ["espada", "basto", "copa", "oro"]
    VALORES = [None, "1", "2", "3", "4", "5", "6", "7", None, None, "10", "11", "12"]

    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo
        self.rank = self.asign_rank()

    def asign_rank(self):
        card_key = (str(self.valor), str(self.palo))
        match card_key:
            case ("1", "0"): return 14
            case ("1", "1"): return 13
            case ("7", "0"): return 12
            case ("7", "3"): return 11
            case ("3", _): return 10
            case ("2", _): return 9
            case ("1", "3"): return 8
            case ("1", "2"): return 8
            case ("12", _): return 7
            case ("11", _): return 6
            case ("10", _): return 5
            case ("6", _): return 3
            case ("5", _): return 2
            case ("4", _): return 1
            case ("7", "2"): return 4
            case ("7", "1"): return 4
            case _: return 0

    def __repr__(self):
        v = self.VALORES[self.valor] +\
            " de " + \
            self.PALOS[self.palo]
        return v 

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


class Player:

    def __init__(self, player):
        self.name = player.display_name
        self.avatar = player.display_avatar
        self.hand = []
        self.points = 0

    def add_card(self, card):       # Agregar una carta
        self.hand.append(card)

    def play_card(self, posicion):          # Jugar una carta
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


class TrucoEmbed:

    def __init__(self, game):
        self.game = game
        self.embed = None

    def create_embed(self):
        embed=discord.Embed(
        title="",
        description="Presioná `Ver cartas` para ver y jugar tu mano.",
        color=0x08ff31,
        type="rich"
        )
        if self.game.mano == self.game.players[0]: 
            mano = self.game.players[0]
            no_mano = self.game.players[1]
        else: 
            mano = self.game.players[1]
            no_mano = self.game.players[0]

        embed.add_field(name="Jugadores", value=f"🖐 {mano.name} - {mano.points} puntos\n👤 {no_mano.name} - {no_mano.points} puntos", inline=True)
        embed.add_field(name="Mesa", value="C1    C2    C3\nC4 C5 C6", inline=True)

        embed.set_author(name=f"Turno de {mano.name}", icon_url=mano.avatar)
        embed.set_footer(text="Bot creado por: BlackFlag", icon_url="https://cdn.discordapp.com/emojis/999830519552426044.webp?size=96&quality=lossless")

        self.embed = embed
        return embed


        

        

class Game:

    def __init__(self, p1, p2, channel):
        self.players = [Player(p1), Player(p2)]
        self.embed = TrucoEmbed(self)
        self.deck = Deck()
        self.truco = False
        self.envido = False
        self.turn = 0
        self.player1_rounds = 0                         
        self.player2_rounds = 0
        self.round = 1
        self.pardas = False
        self.mano = self.players[0]
        self.channel = channel

    async def run_game(self, interaction):
        await self.channel.send(embed=self.embed.create_embed())


    def start_hand(self):           # Crear manos
        print()
        if len(self.deck.cards) < 6: self.deck = Deck()       # Verificar si hay menos de 6 cartas en el mazo, si es así, crear un mazo nuevo
        for player in self.players:
            for _ in range(3):  
                card = self.deck.remove_card_deck()  
                player.add_card(card)
                

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
            self.is_over()
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
                            self.menu(self.truco, self.envido, round, player1)   # Invocar el menu
                            player1_card_played = self.play_round(turn)
                            player1_card_played                             # Invocar metodo para jugar carta
                            turn = 1                                        # Cambiar el turno para que juegue el player 2
                        elif turn==1:
                            self.menu(self.truco, self.envido, round, player2)
                            player2_card_played = self.play_round(turn)
                            player2_card_played
                            turn = 0          
                if player1_card_played.rank > player2_card_played.rank:       # Comparaciones de cartas
                    player1_rounds+=1
                    round+=1
                    print(f"La carta del jugador {player1.name} ({player1_card_played}) es mayor a {player2_card_played}")
                elif player1_card_played.rank < player2_card_played.rank:
                    player2_rounds+=1
                    round+=1
                    print(f"La carta del jugador {player2.name} ({player2_card_played}) es mayor a {player1_card_played}")
                else:                                               # Si es empate = pardas
                     pardas = True
                     round+=1
                     print("Pardas")
            if player1_rounds==2:                                   # Verificar el ganador de la mano
                points_round+=1
                if self.truco: points_round+=1
                print()
                print(f"{player1.name} ganó la mano. +{points_round} puntos")
                player1.points+=points_round
                self.is_over()
                break
            elif player2_rounds==2:
                points_round+=1
                if self.truco: points_round+=1
                print()
                print(f"{player2.name} ganó la mano. +{points_round} puntos")
                player2.points+=points_round
                self.is_over()
                break

    

    def menu(self, truco, envido, round, player):
        print()                                         # Truco/Envido = true -> Ya se jugó, no se puede jugar
        num=-1
        while True:
            if (not truco and not envido and round==1):
                    print(f"\t\t\tTurno de {player.name}")
                    print("-----------------------------------------------------------------------------------------")
                    print(player)
                    print("-----------------------------------------------------------------------------------------")
                    print("-Ingrese 1 para cantar envido")
                    print("-Ingrese 2 para cantar truco")
                    print("-Ingrese 0 para continuar")
                    num=int(input("-> "))
                    match num:
                        case 1:
                            self.cantar_envido(player)
                            self.menu(self.truco, self.envido, round, player)
                        case 2:
                            self.cantar_truco(player)
                            self.menu(self.truco, self.envido, round, player)
                        case 0: break
                        case _:
                            num=int(input("Ingrese el numero correcto -> "))
            elif (truco and not envido and round==1):
                    print(f"\t\t\tTurno de {player.name}")
                    print("-----------------------------------------------------------------------------------------")
                    print(player)
                    print("-----------------------------------------------------------------------------------------")
                    print("-Ingrese 1 para cantar envido")
                    print("-Ingrese 0 para continuar")
                    num=int(input("-> "))
                    if num==1: 
                        self.cantar_envido(player)
                        self.menu(self.truco, self.envido, round, player)
                    elif num==0: break
                    else: num=int(input("Ingrese el numero correcto -> "))
            elif(not truco):
                    print(f"\t\t\tTurno de {player.name}")
                    print("-----------------------------------------------------------------------------------------")
                    print(player)
                    print("-----------------------------------------------------------------------------------------")
                    print("-Ingrese 1 para cantar truco")
                    print("-Ingrese 0 para continuar")
                    num=int(input("-> "))
                    if num==1: 
                        self.cantar_truco(player)
                        self.menu(self.truco, self.envido, round, player)
                    elif num==0: break
                    else: num=int(input("Ingrese el numero correcto -> "))
            elif(truco):
                    print(f"\t\t\tTurno de {player.name}")
                    print("-----------------------------------------------------------------------------------------")
                    print(player)
                    print("-----------------------------------------------------------------------------------------")
                    print("-Ingrese 0 para continuar")
                    num=int(input("-> "))
                    if num==0: break
                    else: num=int(input("Ingrese el numero correcto -> "))
            else:
                continue
            break
            
         
    def cantar_truco(self, player):
        print()
        print(f"{player.name} cantó truco.")
        while True:
            choice = input("Quiero / No quiero (q/nq):").lower()
            if choice == "q" or choice == "nq": break
        if choice == "q": 
             self.truco = True
             print("Truco aceptado")
        else: 
             self.truco = True
             print("Truco no aceptado")


    def cantar_envido(self, player):
        print()
        print(f"{player.name} cantó envido.")
        while True:
            choice = input("Quiero / No quiero (q/nq):").lower()
            if choice == "q" or choice == "nq": break
        if choice == "q": 
             self.envido = True
             print("Envido aceptado")
             self.calculate_envido(self.players[0].hand, self.players[1].hand)
        else: 
             self.envido = True
             print("Envido no aceptado")


    def calculate_envido(self, hand_p1, hand_p2):
        print()
        ind_hand_p1 = [[carta.valor, carta.palo] for carta in hand_p1]
        ind_hand_p2 = [[carta.valor, carta.palo] for carta in hand_p2]
        self.envido = True
        puntos_envido_p1 = 0
        puntos_envido_p2 = 0                                            # No hay flor, los 2 valores mas grandes de la mano se usan en el envido
        if ind_hand_p1[0][1] == ind_hand_p1[1][1]:                              # Verificar si se repiten palos haciendo todas las combinaciones posibles y verificar si alguna carta es 10
            if ind_hand_p1[0][0] >= 10 and ind_hand_p1[1][0] < 10:              # Se podria optimizar muchisimo este codigo para no usar muchos if anidados, pero no supe otra forma para hacerlo mejor
                puntos_envido_p1 = 20 + ind_hand_p1[1][0]
            elif ind_hand_p1[1][0] >= 10 and ind_hand_p1[0][0] < 10:
                puntos_envido_p1 = 20 + ind_hand_p1[0][0]
            elif ind_hand_p1[0][0] >= 10 and ind_hand_p1[1][0] >= 10:
                puntos_envido_p1 = 20
            else:
                puntos_envido_p1 = ind_hand_p1[0][0]+ind_hand_p1[1][0] + 20

        elif ind_hand_p1[0][1] == ind_hand_p1[2][1]:
            if ind_hand_p1[0][0] >= 10 and ind_hand_p1[2][0] < 10:
                puntos_envido_p1 = 20 + ind_hand_p1[2][0]
            elif ind_hand_p1[2][0] >= 10 and ind_hand_p1[0][0] < 10:
                puntos_envido_p1 = 20 + ind_hand_p1[0][0]
            elif ind_hand_p1[0][0] >= 10 and ind_hand_p1[2][0] >= 10:
                puntos_envido_p1 = 20
            else:
                puntos_envido_p1 = ind_hand_p1[0][0]+ind_hand_p1[2][0] + 20
        
        elif ind_hand_p1[1][1] == ind_hand_p1[2][1]:
            if ind_hand_p1[1][0] >= 10 and ind_hand_p1[2][0] < 10:
                puntos_envido_p1 = 20 + ind_hand_p1[2][0]
            elif ind_hand_p1[2][0] >= 10 and ind_hand_p1[1][0] < 10:
                puntos_envido_p1 = 20 + ind_hand_p1[1][0]
            elif ind_hand_p1[1][0] >= 10 and ind_hand_p1[2][0] >= 10:
                puntos_envido_p1 = 20
            else:
                puntos_envido_p1 = ind_hand_p1[1][0]+ind_hand_p1[2][0] + 20
        else:
            valores = [carta[0] for carta in ind_hand_p1]
            for i in valores:
                valores.sort(reverse=True)                     
                puntos_envido_p1 = valores[0]

        if ind_hand_p1[0][1] == ind_hand_p1[1][1] == ind_hand_p1[2][1]:         # Verificar si 3 palos son iguales                                    
                valores = [carta[0] for carta in ind_hand_p1]
                for i in range(3):
                    if valores[i] >= 10:
                        valores.pop(i)       # Crear una lista auxiliar con la mano
                valores.sort(reverse=True)                     # Ordenar la lista de forma descendente, para que los 2 valores mas grandes queden en posicion [0] y [1]
                puntos_envido_p1 = valores[0]+valores[1]+20
        
        if ind_hand_p2[0][1] == ind_hand_p2[1][1]:                              # P2
            if ind_hand_p2[0][0] >= 10 and ind_hand_p2[1][0] < 10:               
                puntos_envido_p2 = 20 + ind_hand_p2[1][0]
            elif ind_hand_p2[1][0] >= 10 and ind_hand_p2[0][0] < 10:
                puntos_envido_p2 = 20 + ind_hand_p2[0][0]
            elif ind_hand_p2[0][0] >= 10 and ind_hand_p2[1][0] >= 10:
                puntos_envido_p2 = 20
            else:
                puntos_envido_p2 = ind_hand_p2[0][0]+ind_hand_p2[1][0] + 20

        elif ind_hand_p2[0][1] == ind_hand_p2[2][1]:
            if ind_hand_p2[0][0] >= 10 and ind_hand_p2[2][0] < 10:
                puntos_envido_p2 = 20 + ind_hand_p2[2][0]
            elif ind_hand_p2[2][0] >= 10 and ind_hand_p2[0][0] < 10:
                puntos_envido_p2 = 20 + ind_hand_p2[0][0]
            elif ind_hand_p2[0][0] >= 10 and ind_hand_p2[2][0] >= 10:
                puntos_envido_p2 = 20
            else:
                puntos_envido_p2 = ind_hand_p2[0][0]+ind_hand_p2[2][0] + 20
        
        elif ind_hand_p2[1][1] == ind_hand_p2[2][1]:
            if ind_hand_p2[1][0] >= 10 and ind_hand_p2[2][0] < 10:
                puntos_envido_p2 = 20 + ind_hand_p2[2][0]
            elif ind_hand_p2[2][0] >= 10 and ind_hand_p2[1][0] < 10:
                puntos_envido_p2 = 20 + ind_hand_p2[1][0]
            elif ind_hand_p2[1][0] >= 10 and ind_hand_p2[2][0] >= 10:
                puntos_envido_p2 = 20
            else:
                puntos_envido_p2 = ind_hand_p2[1][0]+ind_hand_p2[2][0] + 20
        else:
            valores = [carta[0] for carta in ind_hand_p2]
            for i in valores:
                valores.sort(reverse=True)                     
                puntos_envido_p2 = valores[0]

        if ind_hand_p2[0][1] == ind_hand_p2[1][1] == ind_hand_p2[2][1]:                                           
                valores = [carta[0] for carta in ind_hand_p2]
                for i in range(3):
                    if valores[i] >= 10:
                        valores.pop(i)       
                valores.sort(reverse=True)                     
                puntos_envido_p2 = valores[0]+valores[1]+20

        if puntos_envido_p1 > puntos_envido_p2:                                 # Scores
            self.players[0].points += 2
            print(f"Jugador 1: {puntos_envido_p1}")
            print(f"Jugador 2: Son buenas ({puntos_envido_p2})")
            self.is_over()
        elif puntos_envido_p2 > puntos_envido_p1:
            self.players[1].points += 2
            print(f"Jugador 2: {puntos_envido_p2}")
            print(f"Jugador 1: Son buenas ({puntos_envido_p1})")
            self.is_over() 
        else:
            self.players[1].points += 2
            print(f"Jugador 1: {puntos_envido_p1}")
            print(f"Jugador 2: {puntos_envido_p2}")
            self.is_over()


    def play_round(self, pl):
            print()
            while True:
                posicion = int(input("Ingresa la posicion de la carta a jugar: "))
                if posicion in range(3):
                    break
            aux_card_played = self.players[pl].hand[posicion]
            self.players[pl].play_card(posicion)
            return aux_card_played
    

    def reset_hands(self):
        for player in self.players:
            player.hand.clear()
            self.truco = False
            self.envido = False
    

    def is_over(self):
        if self.players[0].points >=30:
            print()
            print(f"El jugador {self.players[0].name} ganó la partida.")
            print(f"Puntos {self.players[0].name}: {self.players[0].points}")
            print(f"Puntos {self.players[1].name}: {self.players[1].points}")
            sys.exit(0)
        elif self.players[1].points >=30:
            print()
            print(f"El jugador {self.players[1].name} ganó la partida.")
            print(f"Puntos {self.players[1].name}: {self.players[1].points}")
            print(f"Puntos {self.players[0].name}: {self.players[0].points}")
            sys.exit(0)
        else:
            return False