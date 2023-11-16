from typing import Optional
import discord
from discord.ext import commands
from truco import Game

class TrucoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
    
    @commands.hybrid_command(name="truco", description="Empezar una partida de truco")
    async def truco(self, ctx: commands.Context, oponente: discord.Member):
        if oponente == ctx.author:
            await ctx.send("No podés empezar una partida con vos mismo.")
            return
        
        view = MainView(truco_cog=self, p1=ctx.author, oponente=oponente, timeout=120)
        embed = discord.Embed(title="Invitación a partida de truco", description="¿Aceptas la partida?", colour=discord.Colour.green())
        await ctx.send(content=f"{ctx.author.mention} te invitó a un truco, {oponente.mention}", embed=embed, view=view)
        await view.wait()


class MainView(discord.ui.View):

    def __init__(self, oponente, p1, truco_cog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.truco_cog = truco_cog
        self.oponente = oponente
        self.p1 = p1

    @discord.ui.button(label="Aceptar", style=discord.ButtonStyle.success)
    async def aceptar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.oponente:
            await interaction.message.edit(content="Partida aceptada, el juego comienza.", view=None, embed=None)
            truco_game = Game(self.p1, self.oponente, interaction.channel)
            await truco_game.run_game(interaction)
            if interaction.channel.id not in self.truco_cog.games:
                self.truco_cog.games[interaction.channel.id] = []
            self.truco_cog.games[interaction.channel.id].append(truco_game)
            #print(self.truco_cog.games)

    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.danger)
    async def rechazar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.oponente:
            await interaction.message.edit(content="Partida rechazada.", view=None, embed=None)

async def setup(bot):
    await bot.add_cog(TrucoCog(bot))

