from random import shuffle
from typing import Optional
import discord
from discord.ext import commands
import asyncio

class Card:

    PALOS = ["Espada", "Basto", "Copa", "Oro"]
    VALORES = [None, "1", "2", "3", "4", "5", "6", "7", None, None, "10", "11", "12"]

    EMOTES = {
    (1, 0): "<:1_De_Espada:1174812805845762190>",
    (1, 1): "<:1_De_Basto:1174812800145707038>",
    (1, 2): "<:1_De_Copa:1174812803220127826>",
    (1, 3): "<:1_De_Oro:1174812809301864528>",
    
    (2, 0): "<:2_De_Espada:1174812379394089091>",
    (2, 1): "<:2_De_Basto:1174812812393058475>",
    (2, 2): "<:2_De_Copa:1174812814947393637>",
    (2, 3): "<:2_De_Oro:1174812380820148304>",
    
    (3, 0): "<:3_De_Espada:1174812388906762240>",
    (3, 1): "<:3_De_Basto:1174812383940722738>",
    (3, 2): "<:3_De_Copa:1174812386457296938>",
    (3, 3): "<:3_De_Oro:1174812392463548416>",
    
    (4, 0): "<:4_De_Espada:1174812400306884720>",
    (4, 1): "<:4_De_Basto:1174812394682323014>",
    (4, 2): "<:4_De_Copa:1174812397790318703>",
    (4, 3): "<:4_De_Oro:1174812401963646976>",
    
    (5, 0): "<:5_De_Espada:1174812410599702690>",
    (5, 1): "<:5_De_Basto:1174812405822406666>",
    (5, 2): "<:5_De_Copa:1174812408112496680>",
    (5, 3): "<:5_De_Oro:1174812414173249628>",
    
    (6, 0): "<:6_De_Espada:1174812423258128454>",
    (6, 1): "<:6_De_Basto:1174812416958288014>",
    (6, 2): "<:6_De_Copa:1174812419806212198>",
    (6, 3): "<:6_De_Oro:1174812425770500146>",
    
    (7, 0): "<:7_De_Espadas:1174812433710325870>",
    (7, 1): "<:7_De_Basto:1174812429155307560>",
    (7, 2): "<:7_De_Copa:1174812432233935038>",
    (7, 3): "<:7_De_Oro:1174812437397110784>",
    
    (10, 0): "<:10_De_Espada:1174812553625477120>",
    (10, 1): "<:10_De_Basto:1174812439754317854>",
    (10, 2): "<:10_De_Copa:1174812442631606322>",
    (10, 3): "<:10_De_Oro:1174812446872059994>",
    
    (11, 0): "<:11_De_Espada:1174812585539948564>",
    (11, 1): "<:11_De_Basto:1174812450474967110>",
    (11, 2): "<:11_De_Copa:1174812452777635870>",
    (11, 3): "<:11_De_Oro:1174812457924042854>",
    
    (12, 0): "<:12_De_Espada:1174812467289923646>",
    (12, 1): "<:12_De_Basto:1174812461099143178>",
    (12, 2): "<:12_De_Copa:1174812464102244492>",
    (12, 3): "<:12_De_Oro:1174812707824873512>",
}

    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo
        self.rank = self.asign_rank()
        self.emote = self.asign_emote()

    
    def asign_emote(self):
        return self.EMOTES.get((self.valor, self.palo), "Emote no encontrado")

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
            case ("7", "2"): return 4
            case ("7", "1"): return 4
            case ("6", _): return 3
            case ("5", _): return 2
            case ("4", _): return 1
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

    async def remove_card_deck(self):          # Remover una carta del mazo
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

    async def add_card(self, card):       # Agregar una carta
        self.hand.append(card)

    async def create_hand_msg(self):
        for card in self.hand:
            chain += f"{card.emote} "
        return chain

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


class GuiView(discord.ui.View):
    
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        
    
    @discord.ui.button(label="Ver Cartas", style=discord.ButtonStyle.success)
    async def cards_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name == self.game.players[0].name:
            content = ""
            for hand in self.game.players[0].hand:
                content += hand.emote
            await interaction.response.send_message(content=content, ephemeral=True, view=self.game.hand_view)

        if interaction.user.display_name == self.game.players[1].name:
            content = ""
            for hand in self.game.players[1].hand:
                content += hand.emote
            await interaction.response.send_message(content=content, ephemeral=True, view=self.game.hand_view)

    @discord.ui.button(label="Irse Al Mazo", style=discord.ButtonStyle.primary)
    async def mazo_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name == self.game.players[0].name:
            button.disabled = True
            self.game.player2_rounds = 2
            self.game.action = f"{self.game.players[0].name} se fue el mazo."
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self)
        if interaction.user.display_name == self.game.players[1].name:
            button.disabled = True
            self.game.player1_rounds = 2
            self.game.action = f"{self.game.players[1].name} se fue el mazo."
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Abandonar Partida", style=discord.ButtonStyle.danger)                     # Player 1 Quit
    async def exit_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name == self.game.players[0].name:
            button.disabled = True
            self.game.players[1].points = self.game.game_mode
            self.game.action = f"{self.game.players[0].name} abandonó la partida. {self.game.players[1].name} gana la partida."
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self)

        if interaction.user.display_name == self.game.players[1].name:                                  # Player 2 Quit
            button.disabled = True
            self.game.players[0].points = self.game.game_mode
            self.game.players[1].points = self.game.game_mode
            self.game.action = f"{self.game.players[1].name} abandonó la partida. {self.game.players[0].name} gana la partida."
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self)
        
    
class HandView(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        
    @discord.ui.button(label="Envido", style=discord.ButtonStyle.primary)
    async def envido_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.round > 1: 
            button.disabled = True
        if button.disabled is not True:
            if interaction.user.display_name == self.game.players[0].name:
                await self.game.envido_embed(self.game.players[0].name, self.game.players[1].name)
            if interaction.user.display_name == self.game.players[1].name:
                await self.game.envido_embed(self.game.players[1].name, self.game.players[0].name)
        button.disabled = True
        await interaction.response.edit_message(view=self)
        

    @discord.ui.button(label="Truco", style=discord.ButtonStyle.primary)
    async def truco_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if button.disabled is not True:
            if interaction.user.display_name == self.game.players[0].name:
                await self.game.truco_embed(self.game.players[0].name, self.game.players[1].name)
            if interaction.user.display_name == self.game.players[1].name:
                await self.game.truco_embed(self.game.players[1].name, self.game.players[0].name)
        button.disabled = True
        await interaction.response.edit_message(view=self)
        

    @discord.ui.button(label=f"Jugar Carta", style=discord.ButtonStyle.success)
    async def play_card_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name == self.game.players[0].name:
            await interaction.response.send_message(content="Clickeá en un botón para jugar esa carta", ephemeral=True, view=self.game.player1_view)
        if interaction.user.display_name == self.game.players[1].name:
            await interaction.response.send_message(content="Clickeá en un botón para jugar esa carta", ephemeral=True, view=self.game.player2_view)


class Player1View(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    
class Player2View(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game


class EnvidoView(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.button(label=f"Quiero", style=discord.ButtonStyle.success)
    async def quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_envido == interaction.user.display_name:
            edit_truco_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title="Envido:", color=0x08ff31, description=self.game.calculate_envido(self.game.players[0].hand, self.game.players[1].hand))
            await edit_truco_embed.edit(embed=embed, view=None)
            await self.game.edit_embed()
            await edit_truco_embed.delete(delay=5)


    @discord.ui.button(label=f"No quiero", style=discord.ButtonStyle.danger)
    async def no_quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

class TrucoView(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.button(label=f"Quiero", style=discord.ButtonStyle.success)
    async def quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label=f"No quiero", style=discord.ButtonStyle.danger)
    async def no_quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

class Game:

    def __init__(self, p1, p2, channel):
        self.opponent_truco = False
        self.opponent_envido = False
        self.canto_envido = False
        self.canto_truco = False
        self.game_mode = 30
        self.truco_view = None
        self.envido_view = None
        self.player1_view = None
        self.player2_view = None
        self.gui_view = None
        self.hand_view = None
        self.players = [Player(p1), Player(p2)]
        self.deck = Deck()
        self.truco = False
        self.envido = False
        self.turn = 0
        self.player1_rounds = 0                         
        self.player2_rounds = 0
        self.player1_card_played = None  
        self.player1_card_played = None
        self.round = 1
        self.pardas = False
        self.mano = self.players[0]
        self.channel = channel
        self.action = "**`Empezó la mano.`**"
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.c5 = None
        self.c6 = None
        self.mesa_msg_id = None
        self.embed_msg_id = None
        self.envido_embed_id = None
        self.truco_embed_id = None


    async def envido_embed(self, player, opponent):
        self.opponent_envido = opponent
        self.canto_envido = True
        envido_embed = discord.Embed(title=f"{player} cantó **envido**.", colour=discord.Colour.green())
        envido_embed = await self.channel.send(embed=envido_embed, view=self.envido_view)
        self.envido_embed_id = envido_embed.id
        return envido_embed
    
    async def truco_embed(self, player, opponent):
        self.opponent_truco = opponent
        self.canto_truco = True
        truco_embed = discord.Embed(title=f"{player} cantó **truco**.", colour=discord.Colour.green())
        truco_embed = await self.channel.send(embed=truco_embed, view=self.truco_view)
        self.truco_embed_id = truco_embed.id
        return truco_embed

    async def create_embed(self):
        embed_msg=discord.Embed(
        title="",
        description="`Empezó la mano.`",
        color=0x08ff31,
        type="rich"
        
        )
        if self.mano == self.players[0]: 
            mano = self.players[0]
            no_mano = self.players[1]
        else: 
            mano = self.players[1]
            no_mano = self.players[0]

        embed_msg.add_field(name="Jugadores", value=f"🖐 *{mano.name}* - **{mano.points} puntos**\n👣 *{no_mano.name}* - **{no_mano.points} puntos**", inline=False)

        embed_msg.set_author(name=f"Turno de {mano.name}", icon_url=mano.avatar)
        embed_msg.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174763587110178887/1174763599474999357/profile.png?ex=6568c6dc&is=655651dc&hm=656cc595ccf8070d9ac77b92c647cd716be55923c9b344c271d2d4dd97a9d9fd&")

        embed_msg = await self.channel.send(embed=embed_msg, view=self.gui_view)
        self.embed_msg_id = embed_msg.id
        return embed_msg
    
    async def edit_embed(self):

        embed_edit=discord.Embed(
        title="",
        description=f"{self.action}",
        color=0x08ff31,
        type="rich"
        
        )

        if self.mano == self.players[0]: 
            mano = self.players[0]
            no_mano = self.players[1]
        else: 
            mano = self.players[1]
            no_mano = self.players[0]
        
        if self.turn == 0: turn = self.players[0]
        else: turn = self.players[1]


        embed_edit.add_field(name="Jugadores", value=f"🖐 *{mano.name}* - **{mano.points} puntos**\n👣 *{no_mano.name}* - **{no_mano.points} puntos**", inline=False)

        embed_edit.set_author(name=f"Turno de {turn.name}", icon_url=turn.avatar)
        embed_edit.set_thumbnail(url="https://cdn.discordapp.com/attachments/1174763587110178887/1174763599474999357/profile.png?ex=6568c6dc&is=655651dc&hm=656cc595ccf8070d9ac77b92c647cd716be55923c9b344c271d2d4dd97a9d9fd&")

        embed_msg = await self.channel.fetch_message(self.embed_msg_id)
        await embed_msg.edit(embed=embed_edit, view=self.gui_view)

    async def create_mesa(self):
        await self.channel.send(content="----------------------\n|               **Mesa**              |\n----------------------")
        mesa_msg = await self.channel.send(content="Sin Cartas")
        self.mesa_msg_id = mesa_msg.id
        return mesa_msg
    
    async def edit_mesa(self):
        mesa_msg = await self.channel.fetch_message(self.mesa_msg_id)
        cards = [self.c1, self.c2, self.c3, self.c4, self.c5, self.c6]
        emotes = [c.emote if c is not None else "" for c in cards]
        content = f"{emotes[0]} {emotes[1]} {emotes[2]}\n\n{emotes[3]} {emotes[4]} {emotes[5]}"
        if content.strip():
            await mesa_msg.edit(content=content)
        else:
            await mesa_msg.edit(content="Sin Cartas")
        
    async def run_game(self, inter):
        self.gui_view = GuiView(game=self)
        self.hand_view = HandView(game=self)
        self.envido_view = EnvidoView(game=self)
        self.truco_view = TrucoView(game=self)
        await self.create_mesa()
        await self.create_embed()
        await self.start_hand()
        await self.edit_mesa()
        await self.edit_embed()
        self.player1_view = Player1View(game=self)
        self.player2_view = Player2View(game=self)
        for card in self.players[0].hand:
            button = discord.ui.Button(label=f"{card}", style=discord.ButtonStyle.secondary, emoji=f"{card.emote}")
            self.player1_view.add_item(button)
        for card in self.players[1].hand:
            button = discord.ui.Button(label=f"{card}", style=discord.ButtonStyle.secondary, emoji=f"{card.emote}")
            self.player2_view.add_item(button)

    async def test(self):
        self.c1=self.players[0].hand[0]
        self.c2=self.players[0].hand[1]
        self.c3=self.players[0].hand[2]
        self.c4=self.players[1].hand[0]
        self.c5=self.players[1].hand[1]

    async def test2(self):
        self.c1=None
        self.c2=None
        self.c3=None
        self.c4=None
        self.c5=None

    async def start_hand(self):           # Crear manos
        if len(self.deck.cards) < 37: self.deck = Deck()      
        for player in self.players:
            for _ in range(3):  
                card = await self.deck.remove_card_deck()  
                await player.add_card(card)
        print(len(self.deck.cards)) 
                

    def hand(self):                                                           
        player1 = self.players[0]
        player2 = self.players[1]
        for _ in range(3):
            self.is_over()
            points_round=0
            if self.player1_rounds!=2 or self.player2_rounds!=2:
                if self.round==3 and self.pardas and self.player1_rounds==1:       # Verificar pardas. Si P1 pardas primera mano y P1 gana segunda mano, P1 gana la mano
                    points_round+=1
                    if self.truco: points_round+=1                     # Verificar si se jugó un truco
                    player1.points+=points_round                    # Sumar los puntos al chico
                    break                                           # Salir del bucle para empezar otra mano
                elif self.round==3 and self.pardas and self.player2_rounds==1:
                    points_round+=1
                    if self.truco: points_round+=1
                    player2.points+=points_round
                    break        
                for _ in range(2):              # Turnos para jugar las cartas. 
                        if self.turn==0:
                            self.player1_card_played = self.play_round(self.turn)
                            self.player1_card_played                             # Invocar metodo para jugar carta
                            self.turn = 1                                        # Cambiar el turno para que juegue el player 2
                        elif self.turn==1:
                            self.player2_card_played = self.play_round(self.turn)
                            self.player2_card_played
                            self.turn = 0          
                if self.player1_card_played.rank > self.player2_card_played.rank:       # Comparaciones de cartas
                    self.player1_rounds+=1
                    self.round+=1
                elif self.player1_card_played.rank < self.player2_card_played.rank:
                    self.player2_rounds+=1
                    self.round+=1
                else:                                               # Si es empate = pardas
                     self.pardas = True
                     self.round+=1
            if self.player1_rounds==2:                                   # Verificar el ganador de la mano
                points_round+=1
                if self.truco: points_round+=1
                player1.points+=points_round
                self.is_over()
                break
            elif self.player2_rounds==2:                                   # Verificar el ganador de la mano
                points_round+=1
                if self.truco: points_round+=1
                player1.points+=points_round
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

    def calculate_envido(self, hand_p1, hand_p2):
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
            i = 0
            while i < len(valores):
                if valores[i] >= 10:
                    valores.pop(i)
                else:
                   i += 1
            valores.sort(reverse=True)
            if len(valores) == 0: puntos_envido_p1 == 20                     
            else: puntos_envido_p1 = valores[0]

        if ind_hand_p1[0][1] == ind_hand_p1[1][1] == ind_hand_p1[2][1]:         # Verificar si 3 palos son iguales                                    
                valores = [carta[0] for carta in ind_hand_p1]
                while i < len(valores):
                    if valores[i] >= 10:
                        valores.pop(i)
                    else:
                        i += 1       
                valores.sort(reverse=True)                     # Ordenar la lista de forma descendente, para que los 2 valores mas grandes queden en posicion [0] y [1]
                if len(valores) == 1: puntos_envido_p1 = valores[0] + 20
                else: puntos_envido_p1 = valores[0]+valores[1]+20
        
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
            i = 0
            while i < len(valores):
                if valores[i] >= 10:
                    valores.pop(i)
                else:
                    i += 1
            valores.sort(reverse=True)                     
            if len(valores) == 0: puntos_envido_p2 == 20                     
            else: puntos_envido_p2 = valores[0]

        if ind_hand_p2[0][1] == ind_hand_p2[1][1] == ind_hand_p2[2][1]:                                           
                valores = [carta[0] for carta in ind_hand_p2]
                while i < len(valores):
                    if valores[i] >= 10:
                        valores.pop(i)
                    else:
                        i += 1       
                valores.sort(reverse=True)                    
                if len(valores) == 1: puntos_envido_p2 = valores[0] + 20
                else: puntos_envido_p2 = valores[0]+valores[1]+20

        if puntos_envido_p1 > puntos_envido_p2: 
            self.players[0].points += 2
            self.action = f"**`{self.players[0].name} ganó el envido`**."
        elif puntos_envido_p2 > puntos_envido_p1: 
            self.players[1].points += 2
            self.action = f"**`{self.players[1].name} ganó el envido`**."
        elif self.mano == self.players[0]: 
            self.players[0].points += 2
            self.action = f"**`{self.players[0].name} ganó el envido`**."
        else: 
            self.players[1] += 2
            self.action = f"**`{self.players[1].name} ganó el envido`**."
        return f"*{self.players[0].name}*: **{puntos_envido_p1}**\n*{self.players[1].name}*: **{puntos_envido_p2}**"


    def play_round(self, pl):
            #aux_card_played = self.players[pl].hand[posicion]
            #self.players[pl].play_card(posicion)
            #return aux_card_played
            pass
    

    def reset_hands(self):
        for player in self.players:
            player.hand.clear()
            self.truco = False
            self.envido = False
    

    def is_over(self):
        if self.players[0].points >=30:
            return True
        elif self.players[1].points >=30:
            return True
        else:
            return False