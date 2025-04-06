print("⚙️ Spongebot main.py gestart")
import discord
from discord.ext import commands
import os
import asyncio

TOKEN = os.environ["DISCORD_TOKEN"]
GUILD_ID = 1356894863454376105

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Ingelogd als {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Commands gesynchroniseerd met GUILD {guild.id} ({len(synced)} commando's)")
    except Exception as e:
        print(f"❌ Sync error: {e}")
    await load_cogs()

async def load_cogs():
    for cog in ["analyse", "dagelijks", "signal"]:
        try:
            await bot.load_extension(f"commands.{cog}")
            print(f"✅ {cog}.py geladen")
        except Exception as e:
            print(f"❌ Fout bij laden {cog}.py: {e}")

async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())