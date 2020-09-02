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
		
	def get_stats(self, member: discord.Member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f"{member.guild.name}"]
		results = collection.find_one({"id": member.id})
		return results
			
	def start_count(self, member: discord.Member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f"{member.guild.name}"]
		time_now = datetime.datetime.now(tz=None).strftime('%d-%m-%Y %H:%M:%S')
		time_str = str(time_now)
		collection.update_one({"id": member.id}, {"$set":{"time": time_str, "count_status": "start"}}, upsert = False)
		print("count started")
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
		print(coins)
		print(time_in_voice_all)
		time = "NO INFO"
		count_status = "stop"
		collection.update_one({"id": member.id}, {"$set":{"coins": coins, "minvoice": minvoice, "count_status": "stop"}}, upsert = False)
		print(f"------------------------------------------------------------------------------------------------------------------------------------\n{member} leaved channel, stats updated\n------------------------------------------------------------------------------------------------------------------------------------")
		return

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before, after, guild=discord.Guild):
		for guild in self.bot.guilds:
			for vc in guild.voice_channels:
				if vc.id != 745611324360228887:
					for member in vc.members:
						coins = self.get_stats(member)
						coins = coins["coins"]
						print(coins)
						if before.channel is None:
							print(len(after.channel.members))
							print(len(after.channel.members) - 1)
							#user joined
							#if users before member joined channel were biggest two
							if len(after.channel.members) - 1 > 2:
								count_status = self.get_stats(member)
								count_status = count_status["count_status"]
								if count_status == "stop":
									self.start_count(member)
							#if users befor member joined were smallest two
							elif len(after.channel.members) >= 2:
								for member in after.channel.members:
									count_status = self.get_stats(member)
									count_status = count_status["count_status"]
									if count_status == "stop":
										print("count started for many members")
										self.start_count(member)

						elif after.channel is None:
							if len(before.channel.members) - 1 > 2:
								count_status = self.get_stats(member)
								count_status = count_status["count_status"]
								if count_status == "start":
									print("count stoped for 1 member")
									self.stop_count(member)
								#if after member leave, users in channel > 2
							elif len(before.channel.members) - 1 < 2:
								print(len(before.channel.members))
								for member in before.channel.members:
									count_status = self.get_stats(member)
									count_status = count_status["count_status"]
									if count_status == "start":
										self.stop_count(member)
										
								count_status = self.get_stats(member)
								count_status = count_status["count_status"]
								if count_status == "start":
									self.stop_count(member)
				else:
					channel = discord.utils.get(guild.voice_channels, name='⡇🔕AFK')
					for member in channel.members:
						count_status = self.get_stats(member)
						count_status = count_status["count_status"]
						if count_status == "start":
							self.stop_count(member)
									
def setup(bot):
	bot.add_cog(VoiceCount(bot))
