from typing import Literal, Optional
import discord
from discord.ext import commands
from truco import Game

class TrucoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_dict = {}     # dict will all current games/players
    
    @commands.hybrid_command(name="truco", description="Empezar una partida de truco")
    async def truco(self, ctx: commands.Context, oponente: discord.Member, puntos: Literal[15, 30]):        # select option from list
        if oponente == ctx.author:
            await ctx.send("No podés empezar una partida con vos msismo.")
            return
        for key in self.game_dict:
            if ctx.author.id in key: 
                await ctx.send(f"{ctx.author.name}, ya estás en una partida.")
                return
            elif oponente.id in key:
                await ctx.send(f"{oponente.name} ya está en una partida.")
                return
        view = MainView(truco_cog=self, p1=ctx.author, oponente=oponente, puntos=puntos, timeout=120)
        embed = discord.Embed(title="Invitación a partida de truco", description="¿Aceptas la partida?", colour=discord.Colour.green())    
        await ctx.send(content=f"{ctx.author.mention} te invitó a un truco, {oponente.mention}", embed=embed, view=view)
        await view.wait()


class MainView(discord.ui.View):

    def __init__(self, oponente, p1, truco_cog, puntos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.truco_cog = truco_cog
        self.oponente = oponente
        self.p1 = p1
        self.puntos = puntos

    @discord.ui.button(label="Aceptar", style=discord.ButtonStyle.success)
    async def aceptar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.oponente:
            await interaction.message.edit(content="Partida aceptada, el juego comienza.", view=None, embed=None)
            truco_game = Game(self.p1, self.oponente, interaction.channel, self.puntos)
            self.truco_cog.game_dict[(self.p1.id, self.oponente.id)] = truco_game       # add players/game to dict
            await truco_game.run_game(interaction)
            del self.truco_cog.game_dict[(self.p1.id, self.oponente.id)]        

    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.danger)
    async def rechazar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.oponente:
            await interaction.message.edit(content="Partida rechazada.", view=None, embed=None)

async def setup(bot):
    await bot.add_cog(TrucoCog(bot))

