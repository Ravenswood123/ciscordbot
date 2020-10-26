import discord
from discord import utils
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import datetime
import random
import os

class Coins(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.mongo_token = os.environ.get("MONGO_TOKEN")
		self.cluster = MongoClient(self.mongo_token)
		self.db = self.cluster["ciscord"]

	@commands.group(name = "coins", invoke_without_command = True)
	async def coinscmd(self, ctx):
		emb = discord.Embed(description="**Коины** - это основная валюта на сервере\nПри общение в голосовых каналах вам будет даватся **1 коин = 1 минута**, при условии, что в воисе сидит ещё как минимум один человек и у вас не выключен микрофон/звук",colour=0x0085FF)
		emb.add_field(name="**``coins balance <участник>``**", value = "Можно узнать ваш баланс коинов", inline=False)
		await ctx.send(embed=emb)
	
	@coinscmd.command(name = "balance")
	async def balance_subcommand(self, ctx, member: discord.Member = None):
		if ctx.channel.id == 747433532770746469:
			if member is None:
				user = ctx.author
			elif member is not None:
				user = member
			collection = self.db[f"{ctx.author.guild.name}"]
			results = collection.find_one({"id": user.id})
			coins = results["coins"]
			status = results["count_status"]
			if status == "stop":
				status = "Начисление остановлено"
			if status == "start":
				status = "Начисление активно"
			hrsvoice = results["minvoice"] // 60
			emb = discord.Embed(title = "Ваша статистика:", colour = 0x0085FF, timestamp = datetime.datetime.now())
			emb.add_field(name = "**:money_with_wings: Количество коинов:**",value = f"{coins}", inline = False)
			emb.add_field(name = "**:clock3: Часы в голосовых каналах:**",value = f"{hrsvoice}", inline = False)
			emb.add_field(name = "**:chart_with_upwards_trend: Статус начисления:**",value = f"{status}", inline = False)
			emb.set_author(name = user.name, icon_url = user.avatar_url)
			await ctx.send(embed = emb)

	@coinscmd.command(name = "send")
	async def send_subcommand(self, ctx, member: discord.Member = None, coins_sum: int = None):
		collection = self.db[f"{ctx.author.guild.name}"]
		if ctx.channel.id == 747433532770746469:
			if coins_sum != None and coins_sum > 0 and member is not None:
				coins = collection.find_one({"id": ctx.author.id})["coins"]
				if coins - coins_sum >= 0:
					collection.update_one({"id": ctx.author.id}, {"$set": {"coins": coins - coins_sum}})
					member_coins = collection.find_one({"id": member.id})["coins"]
					collection.update_one({"id": member.id}, {"$set": {"coins": member_coins + coins_sum}})
					await ctx.message.add_reaction("☑")
			else:
				await ctx.message.delete()
				if member is None:
					emb = discord.Embed(description = f"{ctx.author.mention}, **укажите пользователя** которому нужно сделать перевод", colour = 0x0085FF)
					await ctx.author.send(embed = emb)
				elif coins_sum == None:
					emb = discord.Embed(description = f"{ctx.author.mention}, **укажите сумму** перевода", colour = 0x0085FF)
					await ctx.author.send(embed = emb)
				elif coins_sum < 0:
					emb = discord.Embed(description = f"{ctx.author.mention}, **укажите сумму** перевода больше чем **0**", colour = 0x0085FF)
					await ctx.author.send(embed = emb)
		
	@coinscmd.command(name = "list")
	async def list_subcommand(self, ctx):
		if ctx.channel.id == 747433532770746469:
			collection = self.db[f"{ctx.author.guild.name}"]
			find_result = collection.find().sort("minvoice", -1).limit(10)
			minvoice = []
			users = []
			hrsvoice = []
			for result in find_result:
				member_minvoice = result["minvoice"]
				member_id = result["id"]
				user = self.bot.get_user(member_id)
				minvoice.append(member_minvoice)
				print(user.name)
				users.append(user.name)
			for min in minvoice:
				hrs = min/60
				hrsvoice.append("%.1f" % hrs)
			emb = discord.Embed(description=f"🥇 **{users[0]}** : **{hrsvoice[0]}**\n \n 🥈 **{users[1]}** : **{hrsvoice[1]}**\n \n 🥉 **{users[2]}** : **{hrsvoice[2]}**\n \n 4️⃣ {users[3]} : {hrsvoice[3]}\n \n 5️⃣ {users[4]} : {hrsvoice[4]}\n \n 6️⃣ {users[5]} : {hrsvoice[5]}\n \n 7️⃣ {users[6]} : {hrsvoice[6]}\n \n 8️⃣ {users[7]} : {hrsvoice[7]}\n \n 9️⃣ {users[8]} : {hrsvoice[8]}\n \n 🔟 {users[9]} : {hrsvoice[9]}",colour=0x0085FF, timestamp=datetime.datetime.now())
			emb.set_author(name = "Топ участников по часам в голосовых каналах", icon_url = self.bot.user.avatar_url)
			await ctx.send(embed = emb)

	@coinscmd.command(name = "casino")
	async def casino_subcommand(self, ctx, ammout: int = None):
		if ctx.channel.id == 747433532770746469:
			if ammout is not None: #if users gived ammout
				if ammout >= 50 and ammout <= 5000:
					collection = self.db[f"{ctx.author.guild.name}"]
					coins = collection.find_one({"id": int(ctx.author.id)})["coins"]
					if coins - ammout >= 0:
						casino_members = ["bot", "bot","bot", "bot", "bot", "bot", "member", "member","member","member"]
						winner = random.choice(casino_members)
						print(winner)
						if winner == "bot":
							collection.update_one({"id": ctx.author.id}, {"$set": {"coins": coins - ammout}})
							winner_object = self.bot.user.mention
							print(winner_object)
						elif winner == "member":
							collection.update_one({"id": ctx.author.id}, {"$set": {"coins": coins + ammout}})
							winner_object = ctx.author.mention
							print(winner_object)
						if winner_object is not None:
							emb = discord.Embed(description = f":trophy: Победу одерживает {winner_object}. Его выигрыш состовляет **{ammout}**", colour=0x0085FF, timestamp=datetime.datetime.now())
							await ctx.send(embed = emb)
					else:
						emb = discord.Embed(description = f"{ctx.author.mention}, у вас **недостаточно** коинов чтобы сыграть на сумму **{ammout}**", colour=0x0085FF, timestamp=datetime.datetime.now())
						await ctx.author.send(embed = emb)
				else:
					emb = discord.Embed(description = f"{ctx.author.mention}, сумма ставки должна быть в пороге от **50** до **5000**", colour = 0x0085FF, timestamp=datetime.datetime.now())
					await ctx.author.send(embed = emb)

			elif ammout is None:
				await ctx.message.delete()
				emb = discord.Embed(description = f"{ctx.author.mention}, укажите сумму на которую будете играть", colour=0x0085FF, timestamp=datetime.datetime.now())
				await ctx.author.send(embed = emb)
		
def setup(bot):
	bot.add_cog(Coins(bot))
