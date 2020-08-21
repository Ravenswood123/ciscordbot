import discord
from discord import utils
import pymongo
from pymongo import MongoClient
from discord.ext import commands

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Group Info
	@commands.group(name = 'info', invoke_without_command = True)
	async def infocmd(self, ctx):
		await ctx.send('info')

	#Member Info
	@infocmd.command(name='member', aliases = ['user', 'guildmember'])
	async def member_subcommand(self, ctx, member: discord.Member):
		emb = discord.Embed(title = ':crossed_swords: MEMBER INFORMATION :crossed_swords:', colour = discord.Colour.from_rgb(102, 11, 237))
		bot_name = self.bot.user.name
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f'{member.guild.name}']
		member_coins = collection.find_one({"id": int(member.id)})
		member_coins = member_coins["coins"]
		roles_count = len(member.roles)
		emb.add_field(name = '**Username**', value = f'**``{member}``**')
		emb.add_field(name = '**Id**', value = f'**``{member.id}``**')  
		emb.add_field(name = '**Статус**', value = f'**``{member.status}``**')
		emb.add_field(name = f'**Роли ({roles_count})**', value = f'**``{member.roles}``**')
		emb.add_field(name = '**Активность**', value = f'**``{member.activity}``**')
		emb.add_field(name = '**Дата регистрации**', value = f'**``{member.created_at}``**')
		emb.add_field(name = '**Кол-во коинов**', value=f'**``{member_coins}``**')
		emb.set_thumbnail(url=member.avatar_url)
		await ctx.send(embed = emb )
	#When no argument, member == author
	@member_subcommand.error
	async def member_error(self, ctx, error):
		if isinstance(error, discord.ext.commands.MissingRequiredArgument):
			emb = discord.Embed(title = ':crossed_swords: ИНФОРМАЦИЯ ОБ УЧАСТНИКЕ :crossed_swords:',colour = discord.Colour.from_rgb(102, 11, 237))
			bot_name = self.bot.user.name
			roles_count = len(ctx.author.roles)
			emb.add_field(name = '**Username**', value = f'**``{ctx.author}``**')
			emb.add_field(name = '**Id**', value = f'**``{ctx.author.id}``**')  
			emb.add_field(name = '**Статус**', value = f'**``{ctx.author.status}``**')
			emb.add_field(name = f'**Роли ({roles_count})**', value = f'**``{ctx.author.roles}``**')
			emb.add_field(name = '**Активность**', value = f'**``{ctx.author.activity}``**')
			emb.add_field(name = '**Дата регистрации**', value = f'**``{ctx.author.created_at}``**')
			emb.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed = emb)

	#Channel Info
	@infocmd.command(name='channel', aliases=['channelinfo'])
	async def channel_subcommand(self, ctx):
		channel = ctx.channel
		emb = discord.Embed(title = ':speech_balloon: CHANNEL INFORMATION :speech_balloon:', colour = discord.Colour.from_rgb(102, 11, 237))
		emb.add_field(name = '**Name**', value = f'**``{channel.name}``**', inline = False)
		emb.add_field(name='**Topic**', value=f'**``{channel.topic}``**', inline=False)
		emb.add_field(name='**Id**', value=f'**``{channel.id}``**', inline=False)
		emb.add_field(name='**Category**', value=f'**``{channel.category}``**', inline=False)
		emb.add_field(name='**Position**', value=f'**``{channel.position}``**', inline=False)
		emb.add_field(name='**News Status**', value=f'**``{channel.is_news()}``**', inline = False)
		emb.add_field(name='**News Status**', value=f'**``{channel.is_nsfw()}``**', inline=False)
		emb.add_field(name='**Slowmode Seconds**', value=f'**``{channel.slowmode_delay}``**', inline=False)
		emb.add_field(name='**Created At**', value=f'**``{channel.created_at}``**', inline=False)
		await ctx.send(embed=emb)

#Add cog file
def setup(bot):
	bot.add_cog(Info(bot))