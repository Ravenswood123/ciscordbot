import discord
from discord import utils
import pymongo
import datetime
from pymongo import MongoClient
import json
import os
from discord.ext import commands

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#if bot on
	@commands.Cog.listener()
	async def on_ready(self):
		print(f'------------------------------------------------------------------------------------------------------------------------------------\n{self.bot.user} is Online\n------------------------------------------------------------------------------------------------------------------------------------')
		await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('Главный бот на сервере. !help'))
		#db
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		counter = 0
		for guild in self.bot.guilds:
			collection = db[f"{guild.name}"]
			for member in guild.members:
				#min voice adding
				try:
					minvoice = collection.find_one({"id": int(member.id)})
					minvoice = minvoice["minvoice"]
				except TypeError:
					minvoice = 0

				try:
					coins = collection.find_one({"id": member.id})
					coins = coins["coins"]
				except TypeError:
					coins = 0
				#last time adding
				try:
					time = collection.find_one({"id": member.id})
					time = time["time"]
				except TypeError:
					time = "NO INFO"

				#If user already was in db, update him data
				try:
					post = {"id": member.id, "minvoice": minvoice, "coins": coins, "time": time}
					collection.update_one(post, {'$set': post}, upsert=True)
					counter +=1
				except pymongo.errors.DuplicateKeyError:
					collection.update_one({"id": member.id}, {"$set": {"minvoice": minvoice, "coins": coins, "time": time}})
					counter += 1

		print(f"Adding {counter} data\n------------------------------------------------------------------------------------------------------------------------------------")
	#print all mesages to console
	@commands.Cog.listener()
	async def on_message(self, message, guild: discord.Guild = None):
		guild = message.guild
		print(f'{message.created_at} : {guild.name} : {message.id} : {message.author} : {message.content}')
		if str(message.channel.id) == '746260296720580700':
			await message.add_reaction('👍')
			await message.add_reaction('👎')

	#Get prefix when bot join guild
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open('prefixes.json', 'r') as f:
			prefixes=json.load(f)
		prefixes[str(guild.id)]='$'
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)

	#remove prefixes if bot leave guild
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		with open('prefixes.json', 'r') as f:
			prefixes=json.load(f)
		prefixes.pop(str(guild.id))

	#if incorrent command
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.message.delete()
			emb = discord.Embed(description = f':no_entry_sign: **ОШИБКА** {ctx.author.mention}, неизвестная команда! Вы можите посмотреть доступные команды с помощью ``help``', colour = discord.Colour.from_rgb(102, 11, 23))
			await ctx.send(embed = emb, delete_after=10)
	
	#adding user to database if user join
	@commands.Cog.listener()
	async def on_member_join(self, member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		post = {"id": member.id, "minvoice": 0, "coins": 0, "time": "NO INFO"}
		collection.update_one(post, {'$set': post}, upsert=True)
		print(f"------------------------------------------------------------------------------------------------------------------------------------\n{member} has been joined to server {member.guild.name}, db has been successfuly updated!\n------------------------------------------------------------------------------------------------------------------------------------")

	#remove user database
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		collection.delete_one({"id": member.id, })
		print(f"------------------------------------------------------------------------------------------------------------------------------------\n{member} has been left to server {member.guild.name}, db has been successfuly updated!\n------------------------------------------------------------------------------------------------------------------------------------")
import discord
from discord import utils
import pymongo
import datetime
from pymongo import MongoClient
import json
import os
from discord.ext import commands

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#if bot on
	@commands.Cog.listener()
	async def on_ready(self):
		print(f'------------------------------------------------------------------------------------------------------------------------------------\n{self.bot.user} is Online\n------------------------------------------------------------------------------------------------------------------------------------')
		await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('Главный бот на сервере. !help'))
		#db
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		counter = 0
		for guild in self.bot.guilds:
			collection = db[f"{guild.name}"]
			for member in guild.members:
				#min voice adding
				try:
					minvoice = collection.find_one({"id": int(member.id)})
					minvoice = minvoice["minvoice"]
				except TypeError:
					minvoice = 0

				try:
					coins = collection.find_one({"id": member.id})
					coins = coins["coins"]
				except TypeError:
					coins = 0
				#last time adding
				try:
					time = collection.find_one({"id": member.id})
					time = time["time"]
				except TypeError:
					time = "NO INFO"

				#If user already was in db, update him data
				try:
					post = {"id": member.id, "minvoice": minvoice, "coins": coins, "time": time}
					collection.update_one(post, {'$set': post}, upsert=True)
					counter +=1
				except pymongo.errors.DuplicateKeyError:
					collection.update_one({"id": member.id}, {"$set": {"minvoice": minvoice, "coins": coins, "time": time}})
					counter += 1

		print(f"Adding {counter} data\n------------------------------------------------------------------------------------------------------------------------------------")
	#print all mesages to console
	@commands.Cog.listener()
	async def on_message(self, message, guild: discord.Guild = None):
		guild = message.guild
		print(f'{message.created_at} : {guild.name} : {message.id} : {message.author} : {message.content}')
		if str(message.channel.id) == '746260296720580700':
			await message.add_reaction('👍')
			await message.add_reaction('👎')

	#Get prefix when bot join guild
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open('prefixes.json', 'r') as f:
			prefixes=json.load(f)
		prefixes[str(guild.id)]='$'
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)

	#remove prefixes if bot leave guild
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		with open('prefixes.json', 'r') as f:
			prefixes=json.load(f)
		prefixes.pop(str(guild.id))

	#if incorrent command
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.message.delete()
			emb = discord.Embed(description = f':no_entry_sign: **ОШИБКА** {ctx.author.mention}, неизвестная команда! Вы можите посмотреть доступные команды с помощью ``help``', colour = discord.Colour.from_rgb(102, 11, 23))
			await ctx.send(embed = emb, delete_after=10)
	
	#adding user to database if user join
	@commands.Cog.listener()
	async def on_member_join(self, member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		post = {"id": member.id, "minvoice": 0, "coins": 0, "time": "NO INFO"}
		collection.update_one(post, {'$set': post}, upsert=True)
		print(f"------------------------------------------------------------------------------------------------------------------------------------\n{member} has been joined to server {member.guild.name}, db has been successfuly updated!\n------------------------------------------------------------------------------------------------------------------------------------")

	#remove user database
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		collection.delete_one({"id": member.id, })
		print(f"------------------------------------------------------------------------------------------------------------------------------------\n{member} has been left to server {member.guild.name}, db has been successfuly updated!\n------------------------------------------------------------------------------------------------------------------------------------")
	

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before, after, guild=discord.Guild):
		print(f"было {len(before.channel.members)}")
		print(f"стало {len(after.channel.members)}")

#Add cog files
def setup(bot):
	bot.add_cog(Events(bot))
