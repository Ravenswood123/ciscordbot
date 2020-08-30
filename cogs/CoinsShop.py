import discord
from discord.ext import commands
import os
import datetime
import pymongo
from pymongo import MongoClient

class CoinsShop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	@commands.has_permissions(administrator=True)
	async def shop(self, ctx):
		emb = discord.Embed(description = f"Самая первая версия магазина коинов!\nВы можете покупать роли, нажав на соответствующую реакцию. Предложить свои идеи для ролей в магазине <#746260296720580700>\n \n<@&747361225339568209>\n 1️⃣**``10.000 коинов``**\n \n <@&749492378238320702>\n 2️⃣**``8.500 коинов``**\n \n <@&749283640608817172>\n 3️⃣**``7.500 коинов``**\n \n <@&749491741962272831>\n 4️⃣**``6.000 коинов``**\n \n <@&747361735907737671>\n 5️⃣**``5.000 коинов``**\n \n <@&749491421727424522>\n 6️⃣**``3.500 коинов``**\n \n <@&747345315505373197>\n 7️⃣**``2.500 коинов``**\n \n <@&747361500758409318>\n 8️⃣**``1.500 коинов``**\n \n <@&747345168453206036>\n 9️⃣ **``1.000 коинов``**\n \n <@&749212410128367657>\n 🔟**``1.000 коинов``**\n \n", colour=0xFFC700)
		await ctx.send(embed=emb)
		await ctx.message.add_reaction(f'1️⃣')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		message_id = payload.message_id
		if payload.message_id == 749497348022992897:
			guild_id = payload.guild_id
			guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
			if payload.emoji.name == "1️⃣":
				role = discord.utils.get(guild.roles, name="👑Величайший")
				price = 10000
			elif payload.emoji.name == "2️⃣":
				role = discord.utils.get(guild.roles, name="⚔️ОТСОСАЛИ НАХУЙ 21 КИЛЛ НАХУЙ")
				price = 8500
			elif payload.emoji.name == "3️⃣":
				role = discord.utils.get(guild.roles, name="🦀box like fish")
				price = 7500
			elif payload.emoji.name == "4️⃣":
				role = discord.utils.get(guild.roles, name="🍕кушаю пиццу и смотрю видос ксго коффи")
				price = 6000
			elif payload.emoji.name == "5️⃣":
				role = discord.utils.get(guild.roles, name="🤪долбоеб")
				price = 5000
			elif payload.emoji.name == "6️⃣":
				role = discord.utils.get(guild.roles, name="0️⃣ping")
				price = 3500
			elif payload.emoji.name == "7️⃣":
				role = discord.utils.get(guild.roles, name="🤵🏼VIP")
				price = 2500
			elif payload.emoji.name == "8️⃣":
				role = discord.utils.get(guild.roles, name="💀zxc")
				price = 1500
			elif payload.emoji.name == "9️⃣":
				role = discord.utils.get(guild.roles, name="🗿 Каменный камень")
				price = 1000
			elif payload.emoji.name == "🔟":
				role = discord.utils.get(guild.roles, name="👃Нюхай бебру")
				price = 1000
			if role is not None:
				member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
				if member is not None:
					mongo_token=os.environ.get('MONGO_TOKEN')
					cluster = MongoClient(mongo_token)
					db = cluster["ciscord"]
					collection = db[f'{member.guild.name}']
					coins = collection.find_one({"id": int(member.id)})
					coins = coins["coins"]
					coins = coins - price
					if coins < 0:
						emb = discord.Embed(description = f'У вас недостаточно коинов для преобретения данной роли.',colour=0xFFC700, timestamp=datetime.datetime.now())
						await member.send(embed = emb)
					elif coins >= 0:
						collection.update_one({"id": member.id}, {"$set": {"coins": coins}})
						await member.add_roles(role)
						print("done")
def setup(bot):
	bot.add_cog(CoinsShop(bot))
