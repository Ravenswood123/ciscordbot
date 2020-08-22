import discord
from pymongo import MongoClient
import asyncio
import time
from discord.ext import commands
from discord import utils

class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Test bot command
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def test(self, ctx):
		emb = discord.Embed(description = f's', colour = discord.Colour.from_rgb(102, 11, 237))
		await ctx.send(embed=emb, delete_after=10)

	#Clear command
	@commands.command()
	async def clear(self, ctx, ammout = 100):
		msgs = 0
		async for msg in ctx.channel.history(limit=ammout)
			msgs+=1
		await ctx.channel.purge(limit=ammout+1):ballot_box_with_check:
		emb = discord.Embed(describtion = ":ballot_box_with_check: {ctx.author.mention}, успешно удалено **{msgs}** сообщений!")
		await ctx.send(embed=emb, delete_after=5)
	#Kick command
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def kick(self, ctx, member: discord.Member, *, reason = None):
		await ctx.message.delete()
		await member.kick(reason=reason)
		emb = discord.Embed(description = f':white_check_mark: {member.mention} был **кикнут** с помощью {ctx.author.mention}.', colour = discord.Colour.from_rgb(102, 11, 237))
		await ctx.send(embed = emb)
	@kick.error
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(description = f':no_entry_sign: **ОШИБКА** {ctx.author.mention}, напишите пользователя, который должен быть **кикнут**', colour = discord.Colour.from_rgb(102, 11, 237))
			await ctx.send(embed = emb)
		if isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(description = f':no_entry_sign: **ОШИБКА** {ctx.author.mention}, у вас **недостаточно прав** для вызова этой команды', colour = discord.Colour.from_rgb(102, 11, 237))
			await ctx.send(embed = emb)

	#Ban command
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def ban(self, ctx, member: discord.Member, *, reason = None):
		await ctx.message.delete()
		await member.kick(reason=reason)
		emb = discord.Embed(description = f':white_check_mark: {member.mention} был **исключён навечно** с помощью {ctx.author.mention}.', colour = discord.Colour.from_rgb(102, 11, 237))
		await ctx.send(embed=emb, delete_after=15)
	@ban.error
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			emb = discord.Embed(description = f':no_entry_sign: **ОШИБКА** {ctx.author.mention}, напишите пользователя, который должен быть **исключён навечно**', colour = discord.Colour.from_rgb(102, 11, 237))
			await ctx.send(embed = emb)
		if isinstance(error, commands.MissingPermissions):
			emb = discord.Embed(description = f':no_entry_sign: **ОШИБКА** {ctx.author.mention}, у вас **недостаточно прав** для вызова этой команды', colour = discord.Colour.from_rgb(102, 11, 237))
			await ctx.send(embed = emb)
	
	#Unban 
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def unban(self, ctx, *, member):
		await ctx.message.delete()
		banned_users = await ctx.guild.bans()
		for ban_entry in banned_users:
			user = ban_entry.user
			await ctx.guild.unban(user)
			emb = discord.Embed(description = f':white_check_mark: {user.mention} снова допущен к серверу с помощью {ctx.author.mention}', colour = discord.Colour.from_rgb(217, 152, 39))
			await ctx.send(embed=emb, delete_after=15)

#Add cog file
def setup(bot):
	bot.add_cog(Mod(bot))