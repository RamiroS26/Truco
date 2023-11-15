import discord
from discord.ext import commands

class TrucoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(name="truco", description="Empezar una partida de truco")
    async def truco(self, ctx: commands.Context, oponente: discord.Member):
        if oponente == ctx.author:
            await ctx.send("No podés empezar una partida con vos mismo.")
            return
        
        await ctx.send(f"Te invitaron a una partida {oponente.mention}")
        
        button_aceptar = discord.ui.Button(label="✅ Aceptar", style=discord.ButtonStyle.success)
        button_rechazar = discord.ui.Button(label="❌ Rechazar", style=discord.ButtonStyle.danger)
        
        view = discord.ui.View()
        view.add_item(button_aceptar)
        view.add_item(button_rechazar)
        
        embed = discord.Embed(title="Invitación a partida de truco", description="¿Aceptas la partida?")
        
        message = await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(TrucoCog(bot))

