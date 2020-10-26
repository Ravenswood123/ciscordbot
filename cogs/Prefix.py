import discord
import json
from discord.ext import commands

class Prefix(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	async def prefix(self, ctx, prefix):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes[str(ctx.guild.id)] = prefix
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent = 4)
		emb = discord.Embed(description = f':white_check_mark: Префикс **успешно** смененён на ``{prefix}``', colour=0x0085FF)
		await ctx.send(embed = emb)
def setup(bot):
	bot.add_cog(Prefix(bot))