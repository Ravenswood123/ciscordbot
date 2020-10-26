import discord
from discord.ext import tasks, commands
from discord import utils
import pymongo
from pymongo import MongoClient
import asyncio
import datetime
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo_token = os.environ.get("MONGO_TOKEN")
        self.cluster = MongoClient(self.mongo_token)
        self.db = self.cluster["ciscord"]

    @commands.group(name = "admin", invoke_without_command = True)
    async def admincmd(self, ctx):
        emb = discord.Embed(description = f"Данная группа команд создана лишь для администраторов сервера", colour = 0x0085FF)
        emb.add_field(name = "**``admin mute <участник> <время в секундах>``**", value = "Мьютит участника на определенное время", inline = False)
        emb.add_field(name = "**``admin clear <количество сообщений>``**", value = "Удаляет заданное количество сообщений", inline = False)
        emb.add_field(name = "**``admin kick <участник>``**", value = "Кикает выбранного участника с сервера", inline = False)
        emb.add_field(name = "**``admin ban <участник>``**", value = "Банит выбранного участника с сервера", inline = False)
        emb.add_field(name = "**``admin unban <участник>``**", value = "Снимает бан у выбранного участника с сервера", inline = False)
        await ctx.send(embed = emb)

    async def mute_submission(self, member, mute_time): #background task
        await asyncio.sleep(mute_time) #Wait time to unmute
    @admincmd.command(name = "mute")
    @commands.has_permissions(administrator = True)
    async def mute_subcommand(self, ctx, member: discord.Member, mute_time: int = 1):
        if mute_time < 60: #Check if time < 1 minute
            emb = discord.Embed(description = f"Вы замьючены на сервере на {mute_time} секунд", colour = 0x0085FF, timestamp = datetime.datetime.now())
        else:
            emb = discord.Embed(description = f"Вы замьючены на сервере на {mute_time // 60} минут", colour = 0x0085FF, timestamp = datetime.datetime.now())
        await member.send(embed = emb) #dm message to member
        role = discord.utils.get(member.guild.roles, name = "🤐Mute") #find role
        await member.add_roles(role) #adding role to member
        await self.bot.loop.create_task(asyncio.sleep(mute_time)) #create background task
        await member.remove_roles(role) #remove role after time is up

    @admincmd.command(name = "clear")
    @commands.has_permissions(administrator = True)
    async def clear_subcommand(self, ctx, ammout = 100):
        msgs = 0 #counter for deleted messages
        async for msg in ctx.channel.history(limit = ammout): #couting deleted messages in chat
            msgs+=1
        await ctx.channel.purge(limit = ammout + 1) #clear messages in chat and command call message
        emb = discord.Embed(description = f":ballot_box_with_check: {ctx.author.mention}, успешно удалено **{msgs}** сообщений!", colour = 0x0085FF)
        await ctx.send(embed = emb, delete_after = 5)

    @admincmd.command(name = "kick")
    @commands.has_permissions(administrator = True)
    async def kick_subcommand(self, ctx, member: discord.Member, *, reason = None):
        await ctx.message.delete()
        await member.kick(reason = f"{ctx.author.name} исключил пользователя {member.name}")
        emb = discord.Embed(description = f":white_check_mark: {member.mention} был **кикнут** с помощью {ctx.author.mention}", colour = 0x0085FF)
        await ctx.send(embed = emb, delete_after = 10)
    
    @admincmd.command(name = "ban")
    @commands.has_permissions(administrator = True)
    async def ban_subcommand(self, ctx, member: discord.Member, *, reason = None):
        await ctx.message.delete()
        await member.ban(reason = f"{ctx.author.name} забанил пользователя {member.name}")
        emb = discord.Embed(description = f":white_check_mark: {member.mention} был **кикнут** с помощью {ctx.author.mention}", colour = 0x0085FF)
        await ctx.send(embed = emb, delete_after = 10)

    @admincmd.command(name = "unban")
    async def unban_subcommand(self, ctx, *, member: discord.Member):
        await ctx.message.delete() #deleted author`s message
        banned_users = await ctx.guild.bans() #get banned users list
        async for ban_entry in banned_users: 
            user = ban_entry.user
            if user == member: #if member is mentioned in author message
                print("Founded")
                await ctx.guild.unban(user) #unban
        emb = discord.Embed(description = f":white_check_mark: {user.mention} снова допущен к серверу с помощью {ctx.author.mention}",colour = 0x0085FF)
        await ctx.send(embed = emb, delete_after = 10)
    
    @admincmd.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def remove_subcommand(self, ctx, member: discord.Member, remove_category: str = None, remove_ammout: int = None):
        collection = self.db[f"{ctx.author.guild.name}"]
        if remove_category != None and remove_ammout != None:
            if remove_ammout > 0:
                if remove_category == "coins":
                    collection.update_one({"id": member.id}, {"$inc": {"coins": -remove_ammout}})
                    await ctx.message.add_reaction('☑')
                elif remove_category == "hrs":
                    minvoice = collection.find_one({"id": member.id})["minvoice"]
                    hrsremove_ammout = remove_ammout * 60
                    collection.update_one({"id": member.id}, {"$set": {"minvoice": minvoice - hrsremove_ammout}})
                    await ctx.message.add_reaction('☑')
                elif remove_ammout <= 0:
                    emb = discord.Embed(description = f"{ctx.author.mention}, укажите сумму спысывания больше, чем **0**", colour = 0x0085FF)
                    await ctx.author.send(embed = emb)
        else:
            await ctx.message.delete()
            if member is None:
                emb = discord.Embed(description = f"{ctx.author.mention}, **укажите пользователя**", colour = 0x0085FF)
                await ctx.author.send(embed = emb)
            elif remove_category is None:
                emb = discord.Embed(description = f"{ctx.author.mention}, **укажите категорию** спысывания (**hrs** или **coins**)", colour = 0x0085FF)
                await ctx.author.send(embed = emb)
            elif remove_ammout is None:
                emb = discord.Embed(description = f"{ctx.author.mention}, **укажите сумму** спысывания", colour = 0x0085FF)
                await ctx.author.send(embed = emb)
    
    @admincmd.command(name="add")
    @commands.has_permissions(administrator=True)
    async def add_subcommand(self, ctx, member: discord.Member, add_category: str = None, add_ammout: int = None):
        collection = self.db[f"{ctx.author.guild.name}"]
        if add_category != None and add_ammout != None:
            if add_ammout > 0:
                if add_category == "coins":
                    collection.update_one({"id": member.id}, {"$inc": {coins": add_ammout})
                    await ctx.message.add_reaction('☑')
                elif add_category == "hrs":
                    minvoice = collection.find_one({"id": member.id})["minvoice"]
                    hrsadd_ammout = add_ammout * 60
                    collection.update_one({"id": member.id}, {"$set": {"minvoice": minvoice + hrsadd_ammout}})
                    await ctx.message.add_reaction('☑')
                elif add_ammout <= 0:
                    emb = discord.Embed(description = f"{ctx.author.mention}, **укажите сумму** увеличения больше, чем **0**", colour = 0x0085FF)
                    await ctx.author.send(embed = emb)
        else:
            await ctx.message.delete()
            if add_category is None:
                emb = discord.Embed(description = f"{ctx.author.mention}, **укажите категорию** увеличения (**hrs** или **coins**)", colour = 0x0085FF)
                await ctx.author.send(embed = emb)
            elif add_ammout is None:
                emb = discord.Embed(description = f"{ctx.author.mention}, **укажите сумму** увеличения", colour = 0x0085FF)
                await ctx.author.send(embed = emb)

#Add cog file
def setup(bot): 
	bot.add_cog(Admin(bot))
