import discord
from discord.ext import commands
from discord import app_commands
from utils.ta import analyse_multiple_timeframes

class Analyse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="analyse", description="TA van coin op 6 timeframes (debug)")
    @app_commands.describe(coin="Bijv. kaspa, fet, link")
    async def analyse(self, interaction: discord.Interaction, coin: str):
        print(f"[analyse] Commando gestart voor: {coin}")
        await interaction.response.defer()
        symbol = f"{coin.lower()}usdt"
        try:
            print(f"[analyse] Analyse wordt uitgevoerd voor: {symbol}")
            resultaten = analyse_multiple_timeframes(symbol)
            print(f"[analyse] Resultaten ontvangen: {resultaten}")
            if not resultaten:
                await interaction.followup.send("Geen TA-data beschikbaar.")
                return
            embed = discord.Embed(title=f"Analyse: {coin.upper()}", color=0x00ffcc)
            for tf, data in resultaten.items():
                embed.add_field(
                    name=f"{tf}",
                    value=f"RSI: {data['rsi']:.2f}\nTrend: {data['trend']}\nPrijs: ${data['close']:.5f}",
                    inline=False
                )
            await interaction.followup.send(embed=embed)
            print("[analyse] Embed verzonden")
        except Exception as e:
            foutmelding = f"Fout bij analyse: {str(e)}"
            print(f"[analyse] {foutmelding}")
            await interaction.followup.send(foutmelding)

async def setup(bot):
    await bot.add_cog(Analyse(bot))