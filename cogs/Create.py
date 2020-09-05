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
		overwrite = discord.PermissionOverwrite()
		member_coins = results["coins"]
		print(member_coins)
		name = "⡇" + str(name)
		category = self.bot.get_channel(745596012927909899)
		print(category.name)
		if len(category.voice_channels) + 1 <= 15:
			overwrite.manage_roles = True
			await ctx.author.guild.create_voice_channel(name=name, overwrites = overwrite, category=category)

def setup(bot):
	bot.add_cog(Create(bot))
