from random import shuffle
from typing import Optional
import discord
from discord.ext import commands
import asyncio

class Card:

    # for str representation
    PALOS = ["Espada", "Basto", "Copa", "Oro"]
    VALORES = [None, "1", "2", "3", "4", "5", "6", "7", None, None, "10", "11", "12"]

    # discord id emotes
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

    # debugging
    def asign_emote(self):
        return self.EMOTES.get((self.valor, self.palo), "Emote no encontrado")

    # hierarchy of cards
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

    # str representation
    def __repr__(self):
        v = self.VALORES[self.valor] +\
            " de " + \
            self.PALOS[self.palo]
        return v 


class Deck:

    def __init__(self):
        self.cards = []
        for numero in range(1,13):          # deck creation
            for palo in range(4):
                if numero not in [8,9]:
                    self.cards.append(Card(numero,palo))
        shuffle(self.cards)

    async def remove_card_deck(self):          
        if len(self.cards) == 0:
            return "Deck Empty"
        return self.cards.pop()
    
    def shuffle_deck(self):         
        shuffle(self.cards)
    
    def get_remaining_cards(self):
        return len(self.cards)

    def print_deck(self):       # debugging
        for card in self.cards:
            print(card.rank)


class Player:

    def __init__(self, player):
        self.name = player.display_name
        self.avatar = player.display_avatar
        self.hand = []
        self.points = 0

    async def add_card(self, card):       
        self.hand.append(card)

    async def create_hand_msg(self):        # hand shown in ephemeral
        for card in self.hand:
            chain += f"{card.emote} "
        return chain

    # debugging (delete later)  
    def __repr__(self):     
        hand_info = ", ".join(str(card) for card in self.hand)
        return f"{self.name} | Puntos: {self.points} | Cartas en mano: {len(self.hand)} | Cartas: {hand_info}"


class GuiView(discord.ui.View):
    
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        
    
    @discord.ui.button(label="Ver Cartas", style=discord.ButtonStyle.success)
    async def cards_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name == self.game.players[0].name and not self.game.hay_truco:
            if self.game.turn == 1:
                await self.game.hand_view1.disable_all()
            else: await self.game.hand_view1.enable_all()

        if interaction.user.display_name == self.game.players[1].name and not self.game.hay_truco:
            if self.game.turn == 0:
                await self.game.hand_view2.disable_all()
            else: await self.game.hand_view2.enable_all()

        if interaction.user.display_name == self.game.players[0].name:
            content = ""
            for hand in self.game.players[0].hand:
                content += hand.emote
            await interaction.response.send_message(content=content, ephemeral=True, view=self.game.hand_view1)

        if interaction.user.display_name == self.game.players[1].name:
            content = ""
            for hand in self.game.players[1].hand:
                content += hand.emote
            await interaction.response.send_message(content=content, ephemeral=True, view=self.game.hand_view2)

    @discord.ui.button(label="Abandonar Partida", style=discord.ButtonStyle.danger)                     # player 1 quit
    async def exit_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.display_name == self.game.players[0].name:
            button.disabled = True
            self.game.players[1].points = self.game.game_mode
            self.game.action = f"**`{self.game.players[0].name} abandonó la partida. {self.game.players[1].name} gana la partida.`**"
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self)
            await self.game.end_game()

        if interaction.user.display_name == self.game.players[1].name:                                  # player 2 quit
            button.disabled = True
            self.game.players[0].points = self.game.game_mode
            self.game.action = f"**`{self.game.players[1].name} abandonó la partida. {self.game.players[0].name} gana la partida.`**"
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self)
            await self.game.end_game()
    
    async def disable_all(self):
        for child in self.children:
            child.disabled = True


class HandView1(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        
    @discord.ui.button(label="Envido", style=discord.ButtonStyle.primary)
    async def envido_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.turn == 1: button.disabled = True
        else: button.disabled = False
        if self.game.round > 1: 
            button.disabled = True
        if self.game.envido == True: button.disabled = True
        if button.disabled is not True:
            await self.game.envido_embed(self.game.players[0], self.game.players[1])
        button.disabled = True
        await interaction.response.edit_message(view=self)
        

    @discord.ui.button(label="Truco", style=discord.ButtonStyle.primary)
    async def truco_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.turn == 1: button.disabled = True
        else: button.disabled = False
        if self.game.canto_truco == True: button.disabled = True
        if not button.disabled:
            await self.game.truco_embed(self.game.players[0], self.game.players[1])
        button.disabled = True
        await interaction.response.edit_message(view=self)
        

    @discord.ui.button(label=f"Jugar Carta", style=discord.ButtonStyle.success)
    async def play_card_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.game.turn == 0: 
                await self.game.player1_view.turn_enable()
            await interaction.response.send_message(content="Clickeá en un botón para jugar esa carta", ephemeral=True, view=self.game.player1_view)
   

    @discord.ui.button(label="Irse Al Mazo", style=discord.ButtonStyle.danger)
    async def mazo_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.game.turn == 1: button.disabled = True
            else: button.disabled = False
            if button.disabled is not True:
                button.disabled = True
                self.game.action = f"**`{self.game.players[0].name} se fue el mazo.`**"
                await self.game.edit_embed()
                await asyncio.sleep(2)
                self.game.player2_rounds = 2
            await interaction.response.edit_message(view=self)

    async def disable_all(self):
        for child in self.children:
            child.disabled = True

    
    async def enable_all(self):
        for child in self.children:
            child.disabled = False


class HandView2(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        
    @discord.ui.button(label="Envido", style=discord.ButtonStyle.primary)
    async def envido_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.turn == 0: button.disabled = True
        else: button.disabled = False
        if self.game.round > 1: 
            button.disabled = True
        if button.disabled is not True:
            await self.game.envido_embed(self.game.players[1], self.game.players[0])
        button.disabled = True
        await interaction.response.edit_message(view=self)
        

    @discord.ui.button(label="Truco", style=discord.ButtonStyle.primary)
    async def truco_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.turn == 0: button.disabled = True
        else: button.disabled = False
        if self.game.canto_truco == True: button.disabled = True
        if button.disabled is not True:
            await self.game.truco_embed(self.game.players[1], self.game.players[0])
        button.disabled = True
        await interaction.response.edit_message(view=self)
        

    @discord.ui.button(label=f"Jugar Carta", style=discord.ButtonStyle.success)
    async def play_card_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.game.turn == 1: 
                await self.game.player2_view.turn_enable()
            await interaction.response.send_message(content="Clickeá en un botón para jugar esa carta", ephemeral=True, view=self.game.player2_view)
   

    @discord.ui.button(label="Irse Al Mazo", style=discord.ButtonStyle.danger)
    async def mazo_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.game.turn == 0: button.disabled = True
            else: button.disabled = False
            if button.disabled is not True:
                button.disabled = True
                self.game.action = f"**`{self.game.players[1].name} se fue el mazo.`**"
                await self.game.edit_embed()
                await asyncio.sleep(2)
                self.game.player1_rounds = 2
            await interaction.response.edit_message(view=self)

    async def disable_all(self):
        for child in self.children:
            child.disabled = True

    
    async def enable_all(self):
        for child in self.children:
            child.disabled = False


class Player1View(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
    
    async def turn_disable(self):
        for item in self.children:
            item.disabled = True
        

    async def turn_enable(self):
        for item in self.children:
            item.disabled = False


class Player2View(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    async def turn_disable(self):
        for item in self.children:
            item.disabled = True
    
    async def turn_enable(self):
        for item in self.children:
            item.disabled = False


class DefaultButton(discord.ui.Button):     # cards button

    def __init__(self, game, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.position = position

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.display_name == self.game.players[0].name:
            if self.game.turn == 0:
                self.game.player1_card_played = await self.game.play_round(0, self.position)
                self.game.player1_card_played
                if self.game.c1 is None: self.game.c1 = self.game.player1_card_played
                elif self.game.c2 is None: self.game.c2 = self.game.player1_card_played
                else: self.game.c3 = self.game.player1_card_played
                self.game.player1_view.remove_item(self)
                self.game.action = f"**`{self.game.players[0].name} jugó {self.game.player1_card_played}.`**"
                await self.game.edit_mesa()
                print(f"{self.game.round}, {self.game.c1}, {self.game.c4}")
                if self.game.round == 1 and (not self.game.c1 or not self.game.c4):
                    print("entro1")
                    self.game.turn = 1
                await self.game.edit_embed()
            else: 
                await self.game.player1_view.turn_disable()
            await interaction.response.edit_message(view=self.view)
                
        if interaction.user.display_name == self.game.players[1].name:
            if self.game.turn == 1:
                self.game.player2_card_played = await self.game.play_round(1, self.position)
                self.game.player2_card_played
                self.game.player2_view.remove_item(self)
                if self.game.c4 is None: self.game.c4 = self.game.player2_card_played
                elif self.game.c5 is None: self.game.c5 = self.game.player2_card_played
                else: self.game.c6 = self.game.player2_card_played
                self.game.action = f"**`{self.game.players[1].name} jugó {self.game.player2_card_played}.`**"
                await self.game.edit_mesa()
                print(f"{self.game.round}, {self.game.c1}, {self.game.c4}")
                if self.game.round == 1 and (not self.game.c1 or not self.game.c4):
                    print("entro2")
                    self.game.turn = 0
                await self.game.edit_embed()    
            else: 
                await self.game.player2_view.turn_disable()
            await interaction.response.edit_message(view=self.view)


class EnvidoView(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        self.flag = 2

    @discord.ui.button(label=f"Quiero", style=discord.ButtonStyle.success)
    async def quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_envido.name == interaction.user.display_name:
            self.envido = True
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: Quiero", color=0x08ff31, description=self.game.calculate_envido(self.game.players[0].hand, self.game.players[1].hand))
            await edit_envido_embed.edit(embed=embed, view=None)
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)

    @discord.ui.button(label=f"No quiero", style=discord.ButtonStyle.danger)
    async def no_quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_envido.name == interaction.user.display_name:
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: No quiero", color=0xff0000)
            await edit_envido_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.opponent_envido.name} no aceptó el envido`**"
            self.game.canto_envido.points += 1
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=5)

    @discord.ui.button(label=f"Envido", style=discord.ButtonStyle.blurple)
    async def envido2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_envido.name == interaction.user.display_name:
            self.game.envido = True
            self.game.envido_view = Envido2View(self.game)
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: Envido", color=0xffff00)
            await edit_envido_embed.edit(embed=embed)
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self.game.envido_view)
    
    @discord.ui.button(label=f"Real envido", style=discord.ButtonStyle.blurple)
    async def renvido_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_envido.name == interaction.user.display_name:
            self.game.envido = True
            self.flag = 1
            self.game.envido_view = RealEnvidoView(self.game, self.flag)
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: Real envido", color=0xffff00)
            await edit_envido_embed.edit(embed=embed)
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self.game.envido_view)
    
    @discord.ui.button(label=f"Falta envido", style=discord.ButtonStyle.blurple)
    async def fenvido_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_envido.name == interaction.user.display_name:
            self.game.envido = True
            self.flag = 1
            self.game.envido_view = FaltaEnvidoView(self.game, self.flag)
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: Falta envido", color=0xffff00)
            await edit_envido_embed.edit(embed=embed)
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self.game.envido_view)
    

class Envido2View(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        self.flag = 1

    @discord.ui.button(label=f"Quiero", style=discord.ButtonStyle.success)
    async def quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.canto_envido.name == interaction.user.display_name:
            self.game.envido2 = True
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_envido.name}: Quiero", color=0x08ff31, description=self.game.calculate_envido(self.game.players[0].hand, self.game.players[1].hand))
            await edit_envido_embed.edit(embed=embed, view=None)
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)

    @discord.ui.button(label=f"No quiero", style=discord.ButtonStyle.danger)
    async def no_quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.canto_envido.name == interaction.user.display_name:
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: No quiero", color=0xff0000)
            await edit_envido_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.canto_envido.name} no aceptó el envido`**"
            self.game.opponent_envido.points += 2
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=5)
    
    @discord.ui.button(label=f"Real envido", style=discord.ButtonStyle.blurple)
    async def renvido_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.canto_envido.name == interaction.user.display_name:
            self.game.envido2 = True
            self.flag = 2
            self.game.envido_view = RealEnvidoView(self.game, self.flag)
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_envido.name}: Real envido", color=0xffff00)
            await edit_envido_embed.edit(embed=embed)
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self.game.envido_view)
    
    @discord.ui.button(label=f"Falta envido", style=discord.ButtonStyle.blurple)
    async def fenvido_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.canto_envido.name == interaction.user.display_name:
            self.game.envido2 = True
            self.flag = 2
            self.game.envido_view = FaltaEnvidoView(self.game, self.flag)
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_envido.name}: Falta envido", color=0xffff00)
            await edit_envido_embed.edit(embed=embed)
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self.game.envido_view)


class RealEnvidoView(discord.ui.View):

    def __init__(self, game, flag):
        super().__init__(timeout=None)
        self.game = game
        self.flag = flag

    @discord.ui.button(label=f"Quiero", style=discord.ButtonStyle.success)
    async def quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_envido.name == interaction.user.display_name and self.flag == 2:
            self.game.real_envido = True
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: Quiero", color=0x08ff31, description=self.game.calculate_envido(self.game.players[0].hand, self.game.players[1].hand))
            await edit_envido_embed.edit(embed=embed, view=None)
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)
        
        elif self.game.canto_envido.name == interaction.user.display_name and self.flag == 1:
            self.game.real_envido = True
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_envido.name}: Quiero", color=0x08ff31, description=self.game.calculate_envido(self.game.players[0].hand, self.game.players[1].hand))
            await edit_envido_embed.edit(embed=embed, view=None)
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)

    @discord.ui.button(label=f"No quiero", style=discord.ButtonStyle.danger)
    async def no_quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_envido.name == interaction.user.display_name and self.flag == 2:
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: No quiero", color=0xff0000)
            await edit_envido_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.opponent_envido.name} no aceptó el envido`**"
            if self.game.envido: 
                self.game.canto_envido.points += 2
                if self.game.envido2:
                    self.game.canto_envido.points += 2
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)
        
        elif self.game.canto_envido.name == interaction.user.display_name and self.flag == 1:
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_envido.name}: No quiero", color=0xff0000)
            await edit_envido_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.canto_envido.name} no aceptó el envido`**"
            if self.game.envido: 
                self.game.opponent_envido.points += 2
                if self.game.envido2:
                    self.game.opponent_envido.points += 2
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)
    
    @discord.ui.button(label=f"Falta envido", style=discord.ButtonStyle.blurple)
    async def fenvido_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_envido.name == interaction.user.display_name and self.flag == 2:
            self.game.real_envido = True
            self.flag = 1
            self.game.envido_view = FaltaEnvidoView(self.game, self.flag)
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: Falta envido", color=0x08ff31)
            await edit_envido_embed.edit(embed=embed)
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self.game.envido_view)

        elif self.game.canto_envido.name == interaction.user.display_name and self.flag == 1:
            self.game.real_envido = True
            self.flag = 2
            self.game.envido_view = FaltaEnvidoView(self.game, self.flag)
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_envido.name}: Falta envido", color=0xffff00)
            await edit_envido_embed.edit(embed=embed)
            await self.game.edit_embed()
            await interaction.response.edit_message(view=self.game.envido_view)


class FaltaEnvidoView(discord.ui.View):

    def __init__(self, game, flag):
        super().__init__(timeout=None)
        self.game = game
        self.flag = flag

    @discord.ui.button(label=f"Quiero", style=discord.ButtonStyle.success)
    async def quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.canto_envido.name == interaction.user.display_name and self.flag == 1:
            self.game.falta_envido = True
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_envido.name}: Quiero", color=0x08ff31, description=self.game.calculate_envido(self.game.players[0].hand, self.game.players[1].hand))
            await edit_envido_embed.edit(embed=embed, view=None)
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)

        elif self.game.opponent_envido.name == interaction.user.display_name and self.flag == 2:
            self.game.falta_envido = True
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: Quiero", color=0x08ff31, description=self.game.calculate_envido(self.game.players[0].hand, self.game.players[1].hand))
            await edit_envido_embed.edit(embed=embed, view=None)
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)

    @discord.ui.button(label=f"No quiero", style=discord.ButtonStyle.danger)
    async def no_quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.canto_envido.name == interaction.user.display_name and self.flag == 1:
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_envido.name}: No quiero", color=0xff0000)
            await edit_envido_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.canto_envido.name} no aceptó el envido`**"
            if self.game.envido: 
                self.game.opponent_envido.points += 2
                if self.game.envido2:
                    self.game.opponent_envido.points += 2
                    if self.game.real_envido: self.game.opponent_envido.points += 3
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)
        
        elif self.game.opponent_envido.name == interaction.user.display_name and self.flag == 2:
            edit_envido_embed = await self.game.channel.fetch_message(self.game.envido_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_envido.name}: No quiero", color=0xff0000)
            await edit_envido_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.opponent_envido.name} no aceptó el envido`**"
            if self.game.envido: 
                self.game.canto_envido.points += 2
                if self.game.envido2:
                    self.game.canto_envido.points += 2
                    if self.game.real_envido: self.game.canto_envido.points += 3
            await self.game.edit_embed()
            await edit_envido_embed.delete(delay=3)

class TrucoView(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.button(label=f"Quiero", style=discord.ButtonStyle.success)
    async def quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_truco.name == interaction.user.display_name:
            self.game.hay_truco = False
            edit_truco_embed = await self.game.channel.fetch_message(self.game.truco_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_truco.name}: Quiero", color=0x08ff31)
            await edit_truco_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.opponent_truco.name} aceptó el truco`**"
            self.game.truco = True
            await self.game.edit_embed()
            if self.game.canto_truco.name == self.game.players[0].name: await self.game.hand_view1.enable_all()
            else: await self.game.hand_view2.enable_all()
            await edit_truco_embed.delete(delay=2)

    @discord.ui.button(label=f"No quiero", style=discord.ButtonStyle.danger)
    async def no_quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_truco.name == interaction.user.display_name:
            edit_truco_embed = await self.game.channel.fetch_message(self.game.truco_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_truco.name}: No quiero", color=0xff0000)
            await edit_truco_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.opponent_truco.name} no aceptó el truco`**"
            if self.game.canto_truco == self.game.players[0]: self.game.player1_rounds = 2  #p1 win round if p2 not truco
            else: self.game.player2_rounds = 2           
            await self.game.edit_embed()                 # else p2 win
            await edit_truco_embed.delete(delay=2)
    
    @discord.ui.button(label=f"Quiero Retruco", style=discord.ButtonStyle.blurple)
    async def quiero_retruco_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_truco.name == interaction.user.display_name:
            self.game.truco = True
            self.game.truco_view = RetrucoView(self.game)
            edit_truco_embed = await self.game.channel.fetch_message(self.game.truco_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_truco.name}: Quiero **Retruco**", color=0xffff00)
            await edit_truco_embed.edit(embed=embed)
            await interaction.response.edit_message(view=self.game.truco_view)


class RetrucoView(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
    
    @discord.ui.button(label=f"Quiero", style=discord.ButtonStyle.success)
    async def quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.canto_truco.name == interaction.user.display_name:
            self.game.hay_truco = False
            edit_truco_embed = await self.game.channel.fetch_message(self.game.truco_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_truco.name}: Quiero", color=0x08ff31)
            await edit_truco_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.canto_truco.name} aceptó el retruco`**"
            self.game.retruco = True
            await self.game.edit_embed()
            if self.game.canto_truco.name == self.game.players[0].name: await self.game.hand_view1.enable_all()
            else: await self.game.hand_view2.enable_all()
            await edit_truco_embed.delete(delay=2)

    @discord.ui.button(label=f"No quiero", style=discord.ButtonStyle.danger)
    async def no_quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.canto_truco.name == interaction.user.display_name:
            edit_truco_embed = await self.game.channel.fetch_message(self.game.truco_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_truco.name}: No quiero", color=0xff0000)
            await edit_truco_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.canto_truco.name} no aceptó el retruco`**"
            if self.game.canto_truco == self.game.players[0]: self.game.player1_rounds = 2  
            else: self.game.player2_rounds = 2           
            await self.game.edit_embed()                 
            await edit_truco_embed.delete(delay=2)

    
    @discord.ui.button(label=f"Quiero Vale cuatro", style=discord.ButtonStyle.blurple)
    async def quiero_vale4_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.canto_truco.name == interaction.user.display_name:
            self.game.retruco = True
            self.game.truco_view = ValeCuatroView(self.game)
            edit_truco_embed = await self.game.channel.fetch_message(self.game.truco_embed_id)
            embed = discord.Embed(title=f"{self.game.canto_truco.name}: Quiero **Vale cuatro**", color=0xffff00)
            await edit_truco_embed.edit(embed=embed)
            await interaction.response.edit_message(view=self.game.truco_view)


class ValeCuatroView(discord.ui.View):

    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.button(label=f"Quiero", style=discord.ButtonStyle.success)
    async def quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_truco.name == interaction.user.display_name:
            self.game.hay_truco = False
            edit_truco_embed = await self.game.channel.fetch_message(self.game.truco_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_truco.name}: Quiero", color=0x08ff31)
            await edit_truco_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.opponent_truco.name} aceptó el Vale cuatro`**"
            self.game.vale4 = True
            await self.game.edit_embed()
            if self.game.canto_truco.name == self.game.players[0].name: await self.game.hand_view1.enable_all()
            else: await self.game.hand_view2.enable_all()
            await edit_truco_embed.delete(delay=2)

    @discord.ui.button(label=f"No quiero", style=discord.ButtonStyle.danger)
    async def no_quiero_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.game.opponent_truco.name == interaction.user.display_name:
            edit_truco_embed = await self.game.channel.fetch_message(self.game.truco_embed_id)
            embed = discord.Embed(title=f"{self.game.opponent_truco.name}: No quiero", color=0xff0000)
            await edit_truco_embed.edit(embed=embed, view=None)
            self.game.action = f"**`{self.game.opponent_truco.name} no aceptó el Vale cuatro`**"
            if self.game.canto_truco == self.game.players[0]: self.game.player1_rounds = 2  
            else: self.game.player2_rounds = 2           
            await self.game.edit_embed()                 
            await edit_truco_embed.delete(delay=2)


class Game:

    def __init__(self, p1, p2, channel):
        self.opponent_truco = None
        self.opponent_envido = None
        self.canto_envido = None
        self.canto_truco = None
        self.game_mode = 30
        self.truco_view = None
        self.envido_view = None
        self.player1_view = None
        self.player2_view = None
        self.gui_view = None
        self.hand_view1 = None
        self.hand_view2  = None
        self.players = [Player(p1), Player(p2)]
        self.deck = Deck()
        self.hay_truco = False
        self.truco = False
        self.retruco = False
        self.vale4 = False
        self.envido = False
        self.envido2 = False
        self.real_envido = False
        self.falta_envido = False
        self.turn = 0
        self.player1_rounds = 0                         
        self.player2_rounds = 0
        self.player1_card_played = None  
        self.player2_card_played = None
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
        self.mesa_msg_id1 = None
        self.mesa_msg_id2 = None
        self.embed_msg_id = None
        self.envido_embed_id = None
        self.truco_embed_id = None


    async def envido_embed(self, player, opponent):
        self.opponent_envido = opponent
        self.canto_envido = player
        self.envido = True
        envido_embed = discord.Embed(title=f"{player.name}: **Envido**.", color=0xffff00)
        envido_embed = await self.channel.send(embed=envido_embed, view=self.envido_view)
        self.envido_embed_id = envido_embed.id
        return envido_embed
    
    async def truco_embed(self, player, opponent):
        await self.hand_view1.disable_all()
        await self.hand_view2.disable_all()
        self.opponent_truco = opponent
        self.canto_truco = player
        self.hay_truco = True
        truco_embed = discord.Embed(title=f"{player.name}: **Truco**", color=0xffff00)
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
        mesa_msg2 = await self.channel.send(content="----------------------\n|               **Mesa**              |\n----------------------")
        mesa_msg = await self.channel.send(content="⌧               ⌧             ⌧")
        mesa_msg1 = await self.channel.send(content="⌧               ⌧             ⌧")
        self.mesa_msg_id = mesa_msg.id
        self.mesa_msg_id1 = mesa_msg1.id
        self.mesa_msg_id2 = mesa_msg2.id
        return mesa_msg
    
    async def edit_mesa(self):
        mesa_msg = await self.channel.fetch_message(self.mesa_msg_id)
        mesa_msg1 = await self.channel.fetch_message(self.mesa_msg_id1)
        cards = [self.c1, self.c2, self.c3, self.c4, self.c5, self.c6]
        emotes = [c.emote if c is not None else "" for c in cards]
        content = f"{emotes[0]} {emotes[1]} {emotes[2]}"  
        content1 = f"{emotes[3]} {emotes[4]} {emotes[5]}"
        if content.strip():
            await mesa_msg.edit(content=content)
        else:
            await mesa_msg.edit(content="Sin Cartas")
        if content1.strip():
            await mesa_msg1.edit(content=content1)
        else:
            await mesa_msg1.edit(content="Sin Cartas")
        
    async def run_game(self, inter):
        while not await self.is_game_over():
            self.gui_view = GuiView(game=self)
            self.hand_view1 = HandView1(game=self)
            self.hand_view2 = HandView2(game=self)
            self.envido_view = EnvidoView(game=self)
            self.truco_view = TrucoView(game=self)
            await self.create_mesa()
            await self.create_embed()
            await self.start_hand()
            self.player1_view = Player1View(game=self)
            self.player2_view = Player2View(game=self)
            pos1 = -1
            for card in self.players[0].hand:   # hand, button representation
                pos1 += 1
                self.player1_view.add_item(DefaultButton(self, pos1, label=str(card), style=discord.ButtonStyle.secondary, emoji=f"{card.emote}", custom_id=str(card)))
            pos2 = -1
            for card in self.players[1].hand:
                pos2 += 1
                self.player2_view.add_item(DefaultButton(self, pos2, label=str(card), style=discord.ButtonStyle.secondary, emoji=f"{card.emote}", custom_id=str(card)))

            await self.hand()
            print(self.players[0].points)
            print(self.players[1].points)
            print(await self.is_game_over())
            if not await self.is_game_over(): 
                asyncio.sleep(2)
                await self.reset_hand()
            else: await self.end_game()


    async def end_game(self):    
        await self.gui_view.disable_all()
        await self.hand_view1.disable_all()
        await self.hand_view2.disable_all()
        delete_embed_msg = await self.channel.fetch_message(self.embed_msg_id)
        delete_mesa1_msg = await self.channel.fetch_message(self.mesa_msg_id)
        delete_mesa2_msg = await self.channel.fetch_message(self.mesa_msg_id1)
        delete_mesa3_msg = await self.channel.fetch_message(self.mesa_msg_id2)
        await delete_embed_msg.delete(delay=2)
        await delete_mesa1_msg.delete(delay=2)
        await delete_mesa2_msg.delete(delay=2)
        if self.players[0].points >=30: ganador = self.players[0]
        else: ganador = self.players[1]
        await delete_mesa3_msg.edit(content=f"Partida finalizada. Ganador: **{ganador.name}**" )


    async def reset_hand(self):
        if self.mano == self.players[0]:
            self.mano = self.players[1]
            self.turn = 1
        else:
            self.mano = self.players[0]
            self.turn = 0
        self.opponent_truco = None
        self.opponent_envido = None
        self.canto_envido = None
        self.canto_truco = None
        self.truco_view = None
        self.envido_view = None
        self.player1_view = None
        self.player2_view = None
        self.truco = False
        self.retruco = False
        self.vale4 = False
        self.hay_truco = False
        self.envido = False
        self.envido2 = False
        self.real_envido = False
        self.falta_envido = False
        self.player1_rounds = 0                         
        self.player2_rounds = 0
        self.player1_card_played = None  
        self.player2_card_played = None
        self.round = 1
        self.pardas = False
        self.action = "**`Empezó la mano.`**"
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.c5 = None
        self.c6 = None
        self.players[0].hand.clear()
        self.players[1].hand.clear()
        delete_embed_msg = await self.channel.fetch_message(self.embed_msg_id)
        delete_mesa1_msg = await self.channel.fetch_message(self.mesa_msg_id)
        delete_mesa2_msg = await self.channel.fetch_message(self.mesa_msg_id1)
        delete_mesa3_msg = await self.channel.fetch_message(self.mesa_msg_id2)
        await delete_embed_msg.delete(delay=2)
        await delete_mesa1_msg.delete(delay=2)
        await delete_mesa2_msg.delete(delay=2)
        await delete_mesa3_msg.delete(delay=2)


    async def start_hand(self):           # Crear manos
        if len(self.deck.cards) < 37: self.deck = Deck()      
        for player in self.players:
            for _ in range(3):  
                card = await self.deck.remove_card_deck()  
                await player.add_card(card)

    async def is_game_over(self):
        if (self.players[0].points or self.players[1].points) >= self.game_mode: return True
        else: return False

    async def hand(self):
        player1 = self.players[0]
        player2 = self.players[1]
        flag1 = False
        flag2 = False
        flag3 = False  
        while True:
            points_round=0
            if await self.is_game_over(): break
            if self.player1_rounds!=2 or self.player2_rounds!=2:                        # PARDAS
                if self.round==4 and self.pardas and self.player1_rounds==1:       
                    points_round+=1
                    if self.truco: points_round+=1                     
                    player1.points+=points_round                    
                    self.action = f"**`{player1.name} ganó la mano.`**"
                    break                                          
                elif self.round==3 and self.pardas and self.player2_rounds==1:
                    points_round+=1
                    if self.truco: points_round+=1
                    player2.points+=points_round
                    self.action = f"**`{player2.name} ganó la mano.`**"
                    break

                if not flag1 and (self.c1 is not None and self.c4 is not None):          
                    if self.c1.rank > self.c4.rank:      
                        self.player1_rounds+=1
                        self.round+=1
                        self.turn = 0
                        await self.edit_embed()
                        while True:
                            if await self.is_game_over(): break
                            if self.player2_rounds==2 or self.player1_rounds==2:
                                break  
                            if self.c2 is not None:
                                self.turn = 1
                                await self.edit_embed()
                                break
                            await asyncio.sleep(1)

                    elif self.c4.rank > self.c1.rank:
                        self.player2_rounds+=1
                        self.round+=1
                        self.turn = 1
                        await self.edit_embed()
                        while True:
                            if await self.is_game_over(): break
                            if self.player2_rounds==2 or self.player1_rounds==2:
                                break  
                            if self.c5 is not None:
                                self.turn = 0
                                await self.edit_embed()
                                break
                            await asyncio.sleep(1)
                    else:                                             # Si es empate = pardas
                        self.pardas = True
                        self.round+=1
                        if self.mano == self.players[0]: 
                            self.turn = 0
                            await self.edit_embed()
                            while True:
                                if await self.is_game_over(): break
                                if self.player2_rounds==2 or self.player1_rounds==2:
                                    break  
                                if self.c2 is not None:
                                    self.turn = 1
                                    await self.edit_embed()
                                    break
                                await asyncio.sleep(1)
                        else: 
                            self.turn = 1
                            await self.edit_embed()
                            while True:
                                if await self.is_game_over(): break
                                if self.player2_rounds==2 or self.player1_rounds==2:
                                    break  
                                if self.c5 is not None:
                                    self.turn = 1
                                    await self.edit_embed()
                                    break
                                await asyncio.sleep(1)
                    flag1 = True

                if not flag2 and self.c2 is not None and self.c5 is not None:      
                    if self.c2.rank > self.c5.rank:                 
                        self.player1_rounds+=1
                        self.round+=1
                        self.turn = 0
                        await self.edit_embed()
                        while True:
                            if await self.is_game_over(): break
                            if self.player2_rounds==2 or self.player1_rounds==2:
                                break
                            if self.c3 is not None:
                                self.turn = 1
                                await self.edit_embed()
                                break
                            await asyncio.sleep(1)
                    elif self.c5.rank > self.c2.rank:
                        self.player2_rounds+=1
                        self.round+=1
                        self.turn = 1
                        await self.edit_embed()
                        while True:
                            if await self.is_game_over(): break
                            if self.player2_rounds==2 or self.player1_rounds==2:
                                break
                            if self.c6 is not None:
                                self.turn = 0
                                await self.edit_embed()
                                break
                            await asyncio.sleep(1)
                    else:                                             
                        self.pardas = True
                        self.round+=1
                        await self.edit_embed()
                        if self.mano == self.players[0]: 
                            self.turn = 0
                            while True:
                                if await self.is_game_over(): break
                                if self.player2_rounds==2 or self.player1_rounds==2:
                                    break
                                if self.c3 is not None:
                                    self.turn = 1
                                    await self.edit_embed()
                                    break
                                await asyncio.sleep(1)
                        else: 
                            self.turn = 1
                            await self.edit_embed()
                            while True:
                                if await self.is_game_over(): break
                                if self.player2_rounds==2 or self.player1_rounds==2:
                                    break
                                if self.c6 is not None:
                                    self.turn = 1
                                    await self.edit_embed()
                                    break
                                await asyncio.sleep(1)
                    flag2 = True

                if not flag3 and self.c3 is not None and self.c6 is not None:              
                    if self.c3.rank > self.c6.rank:                 
                        self.player1_rounds+=1
                        self.round+=1
                        await self.edit_embed()
                    elif self.c6.rank > self.c3.rank:
                        self.player2_rounds+=1
                        self.round+=1
                        await self.edit_embed()
                    else:                                             
                        self.pardas = True
                        self.round+=1
                        if self.mano == self.players[0]: self.turn = 0
                        await self.edit_embed()
                    flag3 = True
                
            if self.player1_rounds==2:          # check round winner + points                            
                points_round+=1
                if self.truco: 
                    points_round+=1                         
                    if self.retruco: 
                        points_round+=1
                        if self.vale4: 
                            points_round+=1
                player1.points+=points_round
                self.action = f"**`{player1.name} ganó la mano.`**"
                await self.edit_embed()
                break

            elif self.player2_rounds==2:                               
                points_round+=1
                if self.truco: 
                    points_round+=1
                    if self.retruco:
                        points_round+=1
                        if self.vale4:
                            points_round+=1
                player2.points+=points_round
                self.action = f"**`{player2.name} ganó la mano.`**"
                await self.edit_embed()
                break

            await asyncio.sleep(1)

                

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
                i = 0
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
                i = 0
                while i < len(valores):
                    if valores[i] >= 10:
                        valores.pop(i)
                    else:
                        i += 1       
                valores.sort(reverse=True)                    
                if len(valores) == 1: puntos_envido_p2 = valores[0] + 20
                else: puntos_envido_p2 = valores[0]+valores[1]+20


        def falta_envido(self):
            if puntos_envido_p1 > puntos_envido_p2:
                if (self.players[0].points and self.players[1].points) < 15: self.players[0].points = 30
                elif self.players[0].points >= 15: self.players[0].points += (30-self.players[0].points)       
                else: self.players[0].points += (30-self.players[1].points)
            elif puntos_envido_p2 > puntos_envido_p1:
                if (self.players[0].points and self.players[1].points) < 15: self.players[1].points = 30
                elif self.players[0].points >= 15: self.players[1].points += (30-self.players[0].points)       
                else: self.players[1].points += (30-self.players[1].points) 

        if puntos_envido_p1 > puntos_envido_p2: 
            self.players[0].points += 2
            if self.envido2: self.players[0].points += 2
            if self.real_envido: self.players[0].points += 3
            if self.falta_envido: falta_envido(self)
            self.action = f"**`{self.players[0].name} ganó el envido`**."
        elif puntos_envido_p2 > puntos_envido_p1: 
            self.players[1].points += 2
            if self.envido2: self.players[1].points += 2
            if self.real_envido: self.players[1].points += 3
            if self.falta_envido: falta_envido(self)
            self.action = f"**`{self.players[1].name} ganó el envido`**."
        elif self.mano == self.players[0]: 
            self.players[0].points += 2
            if self.envido2: self.players[0].points += 2
            if self.real_envido: self.players[0].points += 3
            if self.falta_envido: falta_envido(self)
            self.action = f"**`{self.players[0].name} ganó el envido`**."
        else: 
            self.players[1] += 2
            if self.envido2: self.players[1].points += 2
            if self.real_envido: self.players[1].points += 3
            if self.falta_envido: falta_envido(self)
            self.action = f"**`{self.players[1].name} ganó el envido`**."
        return f"*{self.players[0].name}*: **{puntos_envido_p1}**\n*{self.players[1].name}*: **{puntos_envido_p2}**"

    async def play_round(self, pl, position):
        card = self.players[pl].hand[position] 
        return card