import discord
from discord import utils
import pymongo
import datetime
from pymongo import MongoClient
import json
import os
from discord.ext import commands

class VoiceCount(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	def get_members_before_after(self, channel, before, after):
		members_after = len(after.channel.members)
		members_before = len(before.channel.members)
		result = [members_before, members_after]
		return result
	
	def start_count(self, member: discord.Member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f"{member.guild.name}"]
		time_now = datetime.datetime.now(tz=None).strftime('%d-%m-%Y %H:%M:%S')
		time_str = str(time_now)
		collection.update_one({"id": member.id}, {"$set":{"time": time_str}})
		return

	def stop_count(self, member: discord.Member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f"{member.guild.name}"]
		time_join = collection.find_one({"id": member.id})
		time_join = time_join["time"]
		time_join = datetime.datetime.strptime(time_join, "%d-%m-%Y %H:%M:%S")
		time_now = datetime.datetime.now(tz=None).strftime('%d-%m-%Y %H:%M:%S')
		time_now = datetime.datetime.strptime(time_now, "%d-%m-%Y %H:%M:%S")
		time_in_voice_hrs = time_now.hour - time_join.hour
		if time_in_voice_hrs == 0:
			time_in_voice_minute = time_now.minute - time_join.minute
			time_in_voice_all = time_in_voice_minute + time_in_voice_hrs
		else:
			time_in_voice_hrs = time_in_voice_hrs * 60 - time_join.minute
			time_in_voice_all = time_in_voice_hrs + time_now.minute	
		minvoice = collection.find_one({"id": int(member.id)})
		minvoice = minvoice["minvoice"]
		minvoice = minvoice + time_in_voice_all
		#coins before
		coins = collection.find_one({"id": member.id})
		coins = coins["coins"]
		coins = coins + time_in_voice_all
		print(time_in_voice_all)
		collection.update_one({"id": member.id}, {"$set": {"coins": coins, "minvoice": minvoice}})
		print("db updated")
		return

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before, after, guild=discord.Guild):
		for guild in self.bot.guilds:
			for channel in guild.voice_channels:
				if channel.id != 745611324360228887:
					for member in channel.members:
						get_members = self.get_members_before_after(channel, before, after)
						members_before = get_members[0]
						members_after = get_members[1]
						print(f"Было {members_before}")
						print(f"Стало {members_after}")
						
						#When member joined 
						if members_after > members_before:

							#If before changes users in voice was biggest 2, start time for new member
							if members_before > 2:
								new_member=list(set(after.channel.members) - set(before.channel.members))
								for member in new_member:
									self.start_count(member)

							#If before changes users in voice was smaller 2
							elif members_before < 2:
								for member in after.channel.members:
									self.start_count(member)

						#When member leaved
						elif members_after < members_before:
							if members_after > 2:
								#If after leaving member, users in channel > 2, stoping time for leaved member
								leaved_member=list(set(before.channel.members) - set(after.channel.members))
								for member in leaved_member:
									self.stop_count(member)
							elif members_after < 2:
								for member in before.channel.members:
									self.stop_count(member)
								#If after members < 2, stopped for all members
def setup(bot):
	bot.add_cog(VoiceCount(bot))
