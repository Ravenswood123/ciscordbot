import discord
from discord import utils
from discord.ext import commands
import time
import asyncio
import json
import os

#Bot prefix
def get_prefix(client, message):
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)
	return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix, intents = discord.Intents.all())
bot_prefix = get_prefix
bot.remove_command("help")

#load cogs
@bot.command
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
async def unload(ctx, extention):
    bot.unload_extension(f"cogs.{extention}")
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"+ {filename}")

if __name__ == "__main__":
	TOKEN = os.environ.get('CISCORD_TOKEN')
	bot.run(TOKEN)
