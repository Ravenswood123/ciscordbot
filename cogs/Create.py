import discord
from discord import utils
import pymongo
from pymongo import MongoClient
import os
from discord.ext import commands

class Create(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	def get_stats(self, member: discord.Member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f"{member.guild.name}"]
		results = collection.find_one({"id": member.id}) #Find user`s data
		return results
	@commands.group(name='create', invoke_without_command=True)
	async def createcmd(self, ctx):
		emb = discord.Embed(description='Вы можете воспльзоваться функциями данной группа команд для создания. Вы можете создать клан или голосовую комнату за соответствующее количество коинов',colour=0xFFC700)
		await ctx.send(embed=emb)
	
	@createcmd.command(name='vc')
	async def vc_subcommand(self, ctx, name: str = None):
		results = self.get_stats(ctx.author)
		member_coins = results["coins"]
		print(member_coins)
		if member_coins - 5000 >= 0:
			if name is not None:
				name = "⡇" + f"{name}"
				print(name)
				await self.bot.create_voice_channel('warn-logs', category='▬▬▬▬▬Private (10/15)▬▬▬▬')

def setup(bot):
	bot.add_cog(Create(bot))
