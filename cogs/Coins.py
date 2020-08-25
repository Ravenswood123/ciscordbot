import discord
from discord import utils
import pymongo
import datetime
import os
from pymongo import MongoClient
import json
from discord.ext import commands
class Coins(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name='coins', invoke_without_command=True)
	async def coinscmd(self, ctx):
		emb = discord.Embed(description='**Коины - это основная валюта на сервере\nПри общение в голосовых каналах вам будет даватся **1 коин = 1 минута**, при условии того что в воисе сидит ещё как минимум один человек',colour=discord.Colour.from_rgb(102, 11, 237))
		emb.add_field(name='**``coins balance``**',value='можно узнать ваш баланс коинов', inline=False)
		await ctx.send(embed=emb)

	@coinscmd.command(name='balance')
	async def balance_subcommand(self, ctx, member: discord.Member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		coins = collection.find_one({"_id": int(member.id)})
		coins = coins["coins"]
		emb = discord.Embed(description=f'Ваш баланс: {coins} коинов',colour=discord.Colour.from_rgb(102, 11, 237))
		emb.set_author(name = member.name, icon_url=member.avatar_url)
		await ctx.send(embed = emb)

	@balance_subcommand.error
	async def balance_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			mongo_token=os.environ.get('MONGO_TOKEN')
			cluster = MongoClient(mongo_token)
			db = cluster["ciscord"]
			collection = db[f'{ctx.author.guild.name}']
			coins = collection.find_one({"_id": int(ctx.author.id)})
			coins = coins["coins"]
			emb = discord.Embed(description=f'Ваш баланс: {coins} коинов', colour=discord.Colour.from_rgb(102, 11, 237))
			emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=emb)
	@coinscmd.command(name='send')
	async def send_subcommand(self, ctx, member: discord.Member, coins_sum=1):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{ctx.author.guild.name}']
		coins = collection.find_one({"_id": int(ctx.author.id)})
		coins = coins["coins"]
		coins = coins - coins_sum
		if coins < 0:
			emb = discord.Embed(description=f'У вас недостаточно коинов для перевода', colour=discord.Colour.from_rgb(102, 11, 237))
			emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed = emb)
		else:
			collection.update_one({"id": ctx.author.id}, {"$set": {"coins": coins}})
			collection = db[f'{ctx.author.guild.name}']
			member_coins = collection.find_one({"_id": int(member.id)})
			member_coins = member_coins["coins"]
			member_coins = member_coins + coins_sum
			collection.update_one({"_id": member.id}, {"$set": {"coins": member_coins}})
			await ctx.message.add_reaction('☑')

	@coinscmd.command(name='award')
	@commands.has_permissions(administrator=True)
	async def award_subcommand(self, ctx, member: discord.Member, coins_add=1):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		coins = collection.find_one({"_id": int(member.id)})
		coins = coins["coins"]
		coins = coins + coins_add
		collection.update_one({"_id": member.id}, {"$set": {"coins": coins}})
		await ctx.message.add_reaction('☑')

	@coinscmd.command(name='remove')
	@commands.has_permissions(administrator=True)
	async def remove_subcommand(self, ctx, member: discord.Member, coins_remove=1):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		coins = collection.find_one({"_id": int(member.id)})
		coins = coins["coins"]
		coins = coins - coins_remove
		collection.update_one({"_id": member.id}, {"$set": {"coins": coins}})
		await ctx.message.add_reaction('☑')
def setup(bot):
	bot.add_cog(Coins(bot))
