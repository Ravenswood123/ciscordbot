import discord
from discord import utils
import pymongo
from pymongo import MongoClient
import datetime
import os
import random
import json
from discord.ext import commands
class Coins(commands.Cog):
	def __init__(self, bot, mongo_token, cluster):
		self.bot = bot
		
	@commands.group(name='coins', invoke_without_command=True)
	async def coinscmd(self, ctx):
		emb = discord.Embed(description='**Коины** - это основная валюта на сервере\nПри общение в голосовых каналах вам будет даватся **1 коин = 1 минута**, при условии того что в воисе сидит ещё как минимум один человек',colour=0xFFC700)
		emb.add_field(name='**``coins balance <участник>``**' ,value = 'Можно узнать ваш баланс коинов', inline=False)
		await ctx.send(embed=emb)

	@coinscmd.command(name='balance')
	async def balance_subcommand(self, ctx, member: discord.Member):
		if ctx.channel.id == 747433532770746469:
			mongo_token=os.environ.get('MONGO_TOKEN')
			cluster = MongoClient(mongo_token)
			db = cluster["ciscord"]
			collection = db[f'{ctx.author.guild.name}']
			find_results = collection.find_one({"id": int(member.id)})
			coins = find_results["coins"]
			status = find_results["count_status"]
			if status == "stop":
				status = "Начисление остановлено"
			if status == "start":
				status = "Начисление активно"
			minvoice = find_results["minvoice"]
			hrsvoice = minvoice // 60
			emb = discord.Embed(title = 'Ваша статистика:', colour=0xFFC700, timestamp=datetime.datetime.now())
			emb.add_field(name='**:money_with_wings: Количество коинов:**',value=f'{coins}', inline=False)
			emb.add_field(name='**:clock3: Часы в голосовых каналах:**',value=f'{hrsvoice}', inline=False)
			emb.add_field(name='**:chart_with_upwards_trend: Статус начисления:**',value=f'{status}', inline=False)
			emb.set_author(name=member.name, icon_url=member.avatar_url)
			await ctx.send(embed=emb)
		else:
			await ctx.message.delete()
			emb = discord.Embed(description = f'В этом чате **запрещено** использовать комманды! Чат для комманд - <#747433532770746469>',colour=0xFFC700, timestamp=datetime.datetime.now())
			emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed = emb)
	@balance_subcommand.error
	async def balance_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			if ctx.channel.id == 747433532770746469:
				mongo_token=os.environ.get('MONGO_TOKEN')
				cluster = MongoClient(mongo_token)
				db = cluster["ciscord"]
				collection = db[f'{ctx.author.guild.name}']
				find_results = collection.find_one({"id": int(ctx.author.id)})
				coins = find_results["coins"]
				status = find_results["count_status"]
				if status == "stop":
					status = "Начисление остановлено"
				if status == "start":
					status = "Начисление активно"	
				minvoice = find_results["minvoice"]
				hrsvoice = minvoice // 60
				emb = discord.Embed(title = 'Ваша статистика:', colour=0xFFC700, timestamp=datetime.datetime.now())
				emb.add_field(name='**:money_with_wings: Количество коинов:**',value=f'{coins}', inline=False)
				emb.add_field(name='**:clock3: Часы в голосовых каналах:**',value=f'{hrsvoice}', inline=False)
				emb.add_field(name='**:chart_with_upwards_trend: Статус начисления:**',value=f'{status}', inline=False)
				emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
				await ctx.send(embed=emb)
			else:
				await ctx.message.delete()
				emb = discord.Embed(description = f'В этом чате **запрещено** использовать комманды! Чат для комманд - <#747433532770746469>',colour=0xFFC700)
				emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
				await ctx.send(embed = emb, delete_after=15)
	@coinscmd.command(name='send')
	async def send_subcommand(self, ctx, member: discord.Member, coins_sum=1):
		if ctx.channel.id == 747433532770746469:
			mongo_token=os.environ.get('MONGO_TOKEN')
			cluster = MongoClient(mongo_token)
			db = cluster["ciscord"]
			collection = db[f'{ctx.author.guild.name}']
			coins = collection.find_one({"id": int(ctx.author.id)})
			coins = coins["coins"]
			coins = coins - coins_sum
			if coins < 0:
				emb = discord.Embed(description=f'У вас недостаточно коинов для перевода', colour=0xFFC700)
				emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
				await ctx.send(embed = emb)
			else:
				collection.update_one({"id": ctx.author.id}, {"$set": {"coins": coins}})
				collection = db[f'{ctx.author.guild.name}']
				member_coins = collection.find_one({"id": int(member.id)})
				member_coins = member_coins["coins"]
				member_coins = member_coins + coins_sum
				collection.update_one({"id": member.id}, {"$set": {"coins": member_coins}})
				await ctx.message.add_reaction('☑')
		else:
			await ctx.message.delete()
			emb = discord.Embed(description = f'В этом чате **запрещено** использовать комманды! Чат для комманд - <#747433532770746469>',colour=0xFFC700)
			emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed = emb, delete_after=15)

	@coinscmd.command(name='award')
	@commands.has_permissions(administrator=True)
	async def award_subcommand(self, ctx, member: discord.Member, coins_add=1):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		coins = collection.find_one({"id": int(member.id)})
		coins = coins["coins"]
		coins = coins + coins_add
		collection.update_one({"id": member.id}, {"$set": {"coins": coins}})
		await ctx.message.add_reaction('☑')

	@coinscmd.command(name='remove')
	@commands.has_permissions(administrator=True)
	async def remove_subcommand(self, ctx, member: discord.Member, coins_remove=1):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		coins = collection.find_one({"id": int(member.id)})
		coins = coins["coins"]
		coins = coins - coins_remove
		collection.update_one({"id": member.id}, {"$set": {"coins": coins}})
		await ctx.message.add_reaction('☑')
	@coinscmd.command(name='list')
	async def list_subcommand(self, ctx):
		if ctx.channel.id == 747433532770746469:
			mongo_token=os.environ.get('MONGO_TOKEN')
			cluster = MongoClient(mongo_token)
			db = cluster["ciscord"]
			collection = db[f'CisCord']
			find_result = collection.find().sort('minvoice', -1).limit(10)
			minvoice = []
			users = []
			hrsvoice = []
			for result in find_result:
				member_minvoice = result["minvoice"]
				member_id = result["id"]
				user = self.bot.get_user(member_id)
				minvoice.append(member_minvoice)
				users.append(user.name)
			for min in minvoice:
				hrs = min/60
				hrsvoice.append('%.1f' % hrs)
			emb = discord.Embed(description=f'🥇 **{users[0]}** : **{hrsvoice[0]}**\n \n 🥈 **{users[1]}** : **{hrsvoice[1]}**\n \n 🥉 **{users[2]}** : **{hrsvoice[2]}**\n \n 4️⃣ {users[3]} : {hrsvoice[3]}\n \n 5️⃣ {users[4]} : {hrsvoice[4]}\n \n 6️⃣ {users[5]} : {hrsvoice[5]}\n \n 7️⃣ {users[6]} : {hrsvoice[6]}\n \n 8️⃣ {users[7]} : {hrsvoice[7]}\n \n 9️⃣ {users[8]} : {hrsvoice[8]}\n \n 🔟 {users[9]} : {hrsvoice[9]}',colour=0xFFC700, timestamp=datetime.datetime.now())
			emb.set_author(name='Топ участников по часам в голосовых каналах', icon_url=self.bot.user.avatar_url)
			await ctx.send(embed = emb)
		else:
			await ctx.message.delete()
			emb = discord.Embed(description = f'В этом чате **запрещено** использовать комманды! Чат для комманд - <#747433532770746469>',colour=0xFFC700, timestamp=datetime.datetime.now)
			emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed = emb, delete_after=15)
	@coinscmd.command(name='casino')
	async def casino_subcommand(self, ctx, ammout: int = None):
		if ctx.channel.id == 747433532770746469:
			if ammout is None:
				await ctx.message.delete()
				emb = discord.Embed(description = f'{ctx.author.mention}, укажите сумму на которую будете играть',colour=0xFFC700, timestamp=datetime.datetime.now())
				await ctx.author.send(embed = emb)
			else:
				mongo_token=os.environ.get('MONGO_TOKEN')
				cluster = MongoClient(mongo_token)
				db = cluster["ciscord"]
				collection = db[f'{ctx.author.guild.name}']
				coins = collection.find_one({"id": int(ctx.author.id)})
				coins = coins["coins"]
				print(coins)
				if coins - ammout <= 0:
					await ctx.message.delete()
					emb = discord.Embed(description = f'{ctx.author.mention}, у вас **недостаточно** средств, чтобы сыграть на эту сумму',colour=0xFFC700, timestamp=datetime.datetime.now())
					await ctx.author.send(embed = emb)
				else:
					if ammout < 49:
						await ctx.message.delete()
						emb = discord.Embed(description = f'{ctx.author.mention}, минимальная ставка **50** коинов',colour=0xFFC700, timestamp=datetime.datetime.now())
						await ctx.author.send(embed = emb)
					elif ammout > 5000 :
						await ctx.message.delete()
						emb = discord.Embed(description = f'{ctx.author.mention}, максимальная ставка **5000** коинов',colour=0xFFC700, timestamp=datetime.datetime.now())
						await ctx.author.send(embed = emb)
					else:
						casino_members = ['bot', 'bot','bot', 'bot', 'bot', 'bot', 'member','member','member','member']
						winner = random.choice(casino_members)
						if winner == 'bot':
							coins = coins - ammout
							collection.update_one({"id": ctx.author.id}, {"$set": {"coins": coins}})
							emb = discord.Embed(description = f'🏆Победу одерживает {self.bot.user.mention}. Его выигрыш состовляет **{ammout}**',colour=0xFFC700, timestamp=datetime.datetime.now())
							await ctx.send(embed = emb)
						elif winner == 'member':
							coins = coins + ammout
							collection.update_one({"id": ctx.author.id}, {"$set": {"coins": coins}})
							emb = discord.Embed(description = f'🏆 Победу одерживает {ctx.author.mention}. Его выигрыш состовляет **{ammout}**',colour=0xFFC700, timestamp=datetime.datetime.now())
							await ctx.send(embed = emb)
		else:
			await ctx.message.delete()
			emb = discord.Embed(description = f'В этом чате **запрещено** использовать комманды! Чат для комманд - <#747433532770746469>',colour=0xFFC700, timestamp=datetime.datetime.now)
			emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed = emb, delete_after=15)
		
def setup(bot):
	bot.add_cog(Coins(bot, mongo_token, cluster))
