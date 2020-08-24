import discord
from discord.ext import commands
class CoinsShop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def shop(self, ctx):
		emb = discord.Embed(description = f"Самая первая версия магазина коинов!\nВы можете покупать роли, нажав на соответствующую реакцию. Предложить свои идеи для ролей в магазине <#746260296720580700>\n \n<@&747361225339568209>\n 1️⃣**``10.000 коинов``**\n \n <@&747362012861956116>\n 2️⃣**``7.500 коинов``**\n \n <@&747361735907737671>\n 3️⃣**``5.000 коинов``**\n \n <@&747345315505373197>\n 4️⃣**``2.500 коинов``**\n \n <@&747361500758409318>\n 5️⃣**``1.500 коинов``**\n \n <@&747345168453206036>\n 6️⃣ **``1.000 коинов``**\n \n", colour = discord.Colour.from_rgb(102, 11, 237))
		await ctx.send(embed=emb)

	@commands.Cog.listener()
	async def on_raw_reaction_add(payload):
		message_id = payload.message_id
		if message_id == 747366393334333481:
			guild_id = payload.guild_id
			if payload.emoji.name == 'one':
				role = discord.utils.get(guild.roles, name='👑Величайший')
				await member.add_roles(role)
def setup(bot):
	bot.add_cog(CoinsShop(bot))
