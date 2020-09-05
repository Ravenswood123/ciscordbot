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
	
	def buy(self, member: discord.Member, ammout):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f"{member.guild.name}"]
		results = collection.find_one({"id": member.id}) #Find user`s data
		coins = results["coins"] - ammout
		collection.update_one({"id": member.id}, {"$set": {"coins": coins}})
		return True
		
	@commands.group(name='create', invoke_without_command=True)
	async def createcmd(self, ctx):
		emb = discord.Embed(description='Вы можете воспльзоваться функциями данной группа команд для создания. Вы можете создать клан или голосовую комнату за соответствующее количество коинов',colour=0xFFC700)
		await ctx.send(embed=emb)
	
	@createcmd.command(name='vc')
	async def vc_subcommand(self, ctx, name: str = None):
		results = self.get_stats(ctx.author)
		member_coins = results["coins"]
		if name is not None:
			name = "⡇" + str(name)
		else:
			name = "⡇" + str(ctx.author.name)
		category = self.bot.get_channel(745596012927909899)
		if member_coins - 5000 >= 0:
			if len(category.voice_channels) + 1 <= 15:
				buy_result = self.buy(ctx.author, 5000)
				if buy_result == True:
					channel = await ctx.author.guild.create_voice_channel(name = name, category = category)
					await channel.set_permissions(ctx.author, manage_roles = True, manage_channels = True)
					len_voice_channels = len(category.voice_channels)
					category_name = f"▬▬▬▬▬Private ({len_voice_channels}/15)▬▬▬▬"
					await category.edit(name = category_name)
			elif len(category.voice.channels) + 1 > 15:
				await ctx.message.delete()
				emb = discord.Embed(description = f'Максимальное количество голосовых комнат. Подождите удаления комнат, чтобы создать голосовой канал',colour=0xFFC700, timestamp=datetime.datetime.now())
				await ctx.author.send(embed = emb)
		elif member_coins - 5000 < 0:
			await ctx.message.delete()
			emb = discord.Embed(description = f'У вас недостаточно коинов для преобретения **голосовой комнаты**',colour=0xFFC700, timestamp=datetime.datetime.now())
			await ctx.author.send(embed = emb)

def setup(bot):
	bot.add_cog(Create(bot))
