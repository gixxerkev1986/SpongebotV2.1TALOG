import discord
from discord.ext import commands
from discord import app_commands
from utils.ta import analyse_single_timeframe

class Signal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="signal", description="Koop-/verkoopadvies voor coin")
    @app_commands.describe(coin="Bijv. kaspa, fet, link")
    async def signal(self, interaction: discord.Interaction, coin: str):
        await interaction.response.defer()
        symbol = f"{coin.lower()}usdt"
        try:
            data = analyse_single_timeframe(symbol, "1h")
            advies = "Koop" if data["rsi"] < 30 and data["trend"] == "Bullish" else "Wacht"
            embed = discord.Embed(title=f"Signal: {coin.upper()}", color=0x66ff66)
            embed.add_field(name="RSI", value=f"{data['rsi']:.2f}")
            embed.add_field(name="Trend", value=data['trend'])
            embed.add_field(name="Laatste prijs", value=f"${data['close']:.5f}")
            embed.add_field(name="Advies", value=advies)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Fout bij signal: {str(e)}")

async def setup(bot):
    await bot.add_cog(Signal(bot))