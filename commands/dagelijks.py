import discord
from discord.ext import commands
from discord import app_commands
from utils.ta import analyse_single_timeframe

class Dagelijks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dagelijks", description="Dagelijkse TA van coin")
    @app_commands.describe(coin="Bijv. kaspa, fet, link")
    async def dagelijks(self, interaction: discord.Interaction, coin: str):
        await interaction.response.defer()
        symbol = f"{coin.lower()}usdt"
        try:
            data = analyse_single_timeframe(symbol, "1d")
            embed = discord.Embed(title=f"Dagelijkse TA: {coin.upper()}", color=0xffcc00)
            embed.add_field(name="RSI", value=f"{data['rsi']:.2f}")
            embed.add_field(name="Trend", value=data['trend'])
            embed.add_field(name="Laatste prijs", value=f"${data['close']:.5f}")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Fout bij dagelijks: {str(e)}")

async def setup(bot):
    await bot.add_cog(Dagelijks(bot))