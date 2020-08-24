import discord
from discord import utils
import pymongo
import datetime
from pymongo import MongoClient
import json
from discord.ext import commands

class VoiceCount(commands.Cog):
	def __init__(self, bot, db):
		self.bot = bot
		self.db = db

	def get_members_after(self, after):
		try:
			members_after = len(after.channel.members)
		except AttributeError:
			members_after = 0
		return members_after

	def get_members_before(self, before):
		try:
			members_before = len(before.channel.members)
		except AttributeError:
			members_before = 0
		return members_before


	def start_count(self, member: discord.Member):
		collection = self.db[f"{member.guild.name}"]
		time_now = datetime.datetime.now(tz=None).strftime("%d-%m-%Y %H:%M:%S")
		time_str = str(time_now)
		self.collection.update_one({"id": member.id}, {"$set":{"time": time_str}})
		return

	def stop_count(self, member: discord.Member):
		collection = self.db[f"{member.guild.name}"]
		time_join = self.collection.find_one({"id": member.id})
		time_join = time_join["time"]
		time_join = datetime.datetime.strptime(time_join, "%d-%m-%Y %H:%M:%S")
		time_now = datetime.datetime.now(tz=None)
		time_in_voice_hrs = time_now.hour - time_join.hour
		time_in_voice_hrs = time_in_voice_hrs * 60
		time_in_voice_minute = time_now.minute - time_join.minute
		time_in_voice_all = time_in_voice_minute + time_in_voice_hrs
		minvoice = self.collection.find_one({"id": int(member.id)})
		minvoice = minvoice["minvoice"]
		minvoice = minvoice + time_in_voice_all
		#coins before
		coins = self.collection.find_one({"id": member.id})
		coins = coins["coins"]
		coins = coins + time_in_voice_all
		print(time_in_voice_all)
		self.collection.update_one({"id": member.id}, {"$set": {"coins": coins, "minvoice": minvoice}})
		self.collection.update_one({"id": member.id}, {"$set": {"time": "NO INFO"}})
		print("db updated")
		return

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before, after, guild=discord.Guild):
		for guild in self.bot.guilds:
			for vc in guild.voice_channels:
				if vc.id != 745611324360228887:
					for member in vc.members:

						members_after = get_members_after(after)
						print(f"Стало {members_after}")
						members_before = get_members_before(before)
						print(f"Было {members_before}")
						
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