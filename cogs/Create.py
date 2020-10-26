import discord
from discord import utils
import pymongo
from pymongo import MongoClient
import os
import datetime
from discord.ext import commands

class Create(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.mongo_token = os.environ.get("MONGO_TOKEN")
		self.cluster = MongoClient(self.mongo_token)
		self.db = self.cluster["ciscord"]

	def buy(self, member: discord.Member, ammout):
		collection = self.db[f"{member.guild.name}"]
		results = collection.find_one({"id": member.id}) #Find user`s data
		coins = results["coins"] - ammout
		collection.update_one({"id": member.id}, {"$set": {"coins": coins}})
		return True
		
	@commands.group(name='create', invoke_without_command=True)
	async def createcmd(self, ctx):
		emb = discord.Embed(description = "Вы можете воспльзоваться функциями данной группа команд для создания. Вы можете создать клан или голосовую комнату за соответствующее количество коинов", colour = 0x0085FF)
		await ctx.send(embed = emb)
	
	@createcmd.command(name = 'vc')
	async def vc_subcommand(self, ctx, name: str = None):
		collection = self.db[f"{ctx.author.guild.name}"]
		member_coins = collection.find_one({"id": ctx.author.id})["coins"]
		if name is not None:
			name = "⡇" + str(name)
		else:
			name = "⡇" + str(ctx.author.name)
		category = self.bot.get_channel(745596012927909899)
		len_vc = len(category.voice_channels)
		if member_coins - 5000 >= 0 and len_vc + 1 <= 15:
			buy_result = self.buy(ctx.author, 5000)
			if buy_result == True:
				channel = await ctx.author.guild.create_voice_channel(name = name, category = category)
				await channel.set_permissions(ctx.author, manage_roles = True, manage_channels = True, connect = True, speak = True, mute_members = True)
		elif len_vc + 1 > 15:
			await ctx.message.delete()
			emb = discord.Embed(description = f"Максимальное количество голосовых комнат. Подождите удаления комнат, чтобы создать голосовой канал", colour = 0x0085FF, timestamp = datetime.datetime.now())
			await ctx.author.send(embed = emb)
		elif member_coins - 5000 < 0:
			await ctx.message.delete()
			emb = discord.Embed(description = f"{ctx.author.mention}, у вас недостаточно коинов для преобретения **голосовой комнаты**", colour = 0x0085FF, timestamp = datetime.datetime.now())
			await ctx.send(embed = emb, delete_after = 5)

def setup(bot):
	bot.add_cog(Create(bot))
