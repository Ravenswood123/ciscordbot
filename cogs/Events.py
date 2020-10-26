import discord
from discord import utils
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import datetime
import asyncio
import datetime
import json
import os

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.mongo_token = os.environ.get("MONGO_TOKEN")
		self.cluster = MongoClient(self.mongo_token)
		self.db = self.cluster["ciscord"]

	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.change_presence(status = discord.Status.online, activity = discord.Game("Главный бот на сервере. !help"))
		print("-" * 130 + f"\n{self.bot.user} online!\n" + "-" * 130)
		counter = 0
		for guild in self.bot.guilds:
			collection = self.db[f"CisCordTest"]
			for member in guild.members:
				if collection.count_documents == 0:
					collection.insert_one({"id": member.id}, {
						"minvoice": 0,
						"coins": 0,
						"time": "NO INFO",
						"count_status": "stop"
					})
					counter += 1
		print(f"Adding {counter} new data\n" + "-" * 130)		

	#print all messages in console
	@commands.Cog.listener()
	async def on_message(self, message, guild: discord.Guild = None):
		guild = message.guild
		print(f"{message.created_at} : {guild.name} : {message.id} : {message.author} : {message.content}\n" + "-" * 130)
		channels_id = [770150613199618069, 746260296720580700]
		if message.channel.id in channels_id: #adding reactions for messages in current channel
			await message.add_reaction("👍")
			await message.add_reaction("👎")

	#get prefix when bot join guild
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open("prefixes.json", "r") as f:
			prefixes = json.load(f)
		prefixes[str(guild.id)]="$"
		with open("prefixes.json", "w") as f:
			json.dump(prefixes, f, indent = 4)

	#remove prefixes if bot leave guild
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		with open("prefixes.json", "r") as f:
			prefixes = json.load(f)
		prefixes.pop(str(guild.id))

	#if incorrent command
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.message.delete()
			emb = discord.Embed(description = f":no_entry_sign: **ОШИБКА** {ctx.author.mention}, неизвестная команда! Вы можите посмотреть доступные команды с помощью ``help``", colour = 0x0085FF)
			await ctx.send(embed = emb, delete_after = 10)
			
	@commands.Cog.listener()
	async def on_command(self, ctx):
		if ctx.channel.id != 747433532770746469 and ctx.command.full_parent_name == "coins": #Checked if command called in current chat
			await ctx.message.delete()
			emb = discord.Embed(description = f"В этом чате **запрещено** использовать комманды! Чат для комманд - <#747433532770746469>", colour = 0x0085FF)
			emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
			await ctx.send(embed = emb, delete_after = 5)

	#adding user to database if user join
	@commands.Cog.listener()
	async def on_member_join(self, member):
		collection = self.db[f"{member.guild.name}"]
		post = {"id": member.id, "minvoice": 0, "coins": 0, "time": "NO INFO", "count_status": "stop"}
		collection.update_one(post, {"$set": post}, upsert = True)
		print(f"{member} has been joined to server {member.guild.name}, db has been successfuly updated!\n" + "-" * 130)

	#remove user database
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		collection = self.db[f"{member.guild.name}"]
		collection.delete_one({"id": member.id, })
		print(f"{member} has been left to server {member.guild.name}, db has been successfuly updated!\n" + "-" * 130)
	
	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		category = channel.category
		privete_channels_category = self.bot.get_channel(745596012927909899)
		if category == privete_channels_category:
			category_name = f"▬▬▬▬▬Private ({len(category.channels)}/15)▬▬▬▬"
			print(category_name)
			print("Channel was delete from private category. Updating counter channels...\n" + "-" * 130)
			await category.edit(name = category_name)

	@commands.Cog.listener()
	async def on_guild_channel_create(self, channel):
		category = channel.category
		privete_channels_category = self.bot.get_channel(745596012927909899)
		if category == privete_channels_category:
			category_name = f"▬▬▬▬▬Private ({len(category.channels)}/15)▬▬▬▬"
			print("New channel on private category created! Updating counter channels...\n" + "-" * 130)
			await category.edit(name = category_name)

#Add cog files
def setup(bot):
	bot.add_cog(Events(bot))
