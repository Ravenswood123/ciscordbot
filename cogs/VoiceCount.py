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
		results = collection.find_one({"id": member.id}) #Find user`s data
		return results
			
	def start_count(self, member: discord.Member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f"{member.guild.name}"]
		time_now = datetime.datetime.now(tz=None).strftime('%d-%m-%Y %H:%M:%S') #Setting now time
		time_str = str(time_now) #Formating datetime to string
		collection.update_one({"id": member.id}, {"$set":{"time": time_str, "count_status": "start"}}, upsert = False) #Updating db
		print("count started")
		return

	def stop_count(self, member: discord.Member):
		mongo_token=os.environ.get('MONGO_TOKEN')
		cluster = MongoClient(mongo_token)
		db = cluster["ciscord"]
		collection = db[f"{member.guild.name}"]
		time_join = collection.find_one({"id": member.id}) #Find user`s data
		time_join = time_join["time"]
		time_join = datetime.datetime.strptime(time_join, "%d-%m-%Y %H:%M:%S") #Formating time in db to datetime format
		time_now = datetime.datetime.now(tz=None).strftime('%d-%m-%Y %H:%M:%S') #Getting now time in db time format
		time_now = datetime.datetime.strptime(time_now, "%d-%m-%Y %H:%M:%S") #String to datetime format
		time_in_voice_hrs = time_now.hour - time_join.hour #Getting hours difference
		if time_in_voice_hrs == 0: #if not an hour has passed
			time_in_voice_minute = time_now.minute - time_join.minute #Getting minutes difference
			time_in_voice_all = time_in_voice_minute #Time in voice == munutes
		elif time_in_voice_hrs < 0:
			time_in_voice_all =  (24 * 60) - (time_join.hour*60 + time_join.minute) + time_now.hour*60 + time_now.minute #Getting minutes difference
		elif time_in_voice_hrs > 0:
			time_in_voice_hrs = time_in_voice_hrs * 60 - time_join.minute #Formating hours to minutes
			time_in_voice_all = time_in_voice_hrs + time_now.minute	 #Minutes in now hour adding minutes in hours
		results = self.get_stats(member) 
		minvoice = results["minvoice"] #Getting mintus before
		minvoice = minvoice + time_in_voice_all #Adding new data to before data
		coins = results["coins"] #Getting coins before
		coins = coins + time_in_voice_all #Adding new data to before data
		print(coins)
		print(time_in_voice_all)
		time = "NO INFO"
		count_status = "stop"
		collection.update_one({"id": member.id}, {"$set":{"coins": coins, "minvoice": minvoice, "count_status": "stop"}}, upsert = False) #Updating db
		return

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before, after, guild=discord.Guild):
		for guild in self.bot.guilds:
			for vc in guild.voice_channels: 
				if vc.id != 745611324360228887: #Checking if channel != afk and member not muted
					for member in vc.members:
						stats = self.get_stats(member)
						if stats["count_status"] == "stop":
							if member.voice.self_mute == False:
								try:
									if member.voice.self_mute == False:
										if before.channel == after.channel: # If user now unmuted, before muted
											if len(after.channel.members) - 1 >= 2: #If count stopped for 1 member, start for him
												self.start_count(member)

											elif len(after.channel.members) >= 2: #If count stopped for all, start count for all
												for member in after.channel.members: #Started count for all
													self.start_count(member)
										if len(after.channel.members) >= 2 and len(before.channel.members) < 2: #If member moved, in before channel users < 2, after users > 2
											for member in after.channel.members: #Checks all members in vc
												self.start_count(member)
								finally:
									if before.channel is None: #Check for user joined
										if len(after.channel.members) - 1 >= 2: #If after biggest two before user join
											self.start_count(member)

										elif len(after.channel.members) >= 2: #Elif after biggest two, before smallest two
											for member in after.channel.members: #Checks all member in vc
												self.start_count(member)

						elif stats["count_status"] == "start": #Elif count already started
							try: # 
								if before.channel == after.channel: #If member muted
									if member.voice.self_mute == True:
										if len(after.channel.members) - 1 < 2: #If other users < 2
											for member in after.channel.members: #Stopping count for all
												self.stop_count(member)
										elif len(after.channel.members) - 1 >= 2: #Elif other users > 2
											self.stop_count(member) #Stopping count for 1 member
								if len(after.channel.members) < 2 and len(before.channel.members) >= 2: #If member moved
									for member in before.channel.members:#Checks all member in vc
									self.stop_count(member)

							else:
								if after.channel is None: #if member leaved
									if len(before.channel.members) - 1 < 2: #If members before leave < 2
										for member in before.channel.members: #Checks all members in vc
											self.stop_count(member)
									elif len(before.channel.members) - 1 >= 2:
										self.stop_count(member) #Stopping count for 1 member
			elif vc.id == 745611324360228887:
				stats = self.get_stats(member)
				if stats["count_status"] == "start":
					afk_channel = discord.utils.get(guild.voice_channels, name='⡇🔕AFK') #Getting afk channel object
					for member in afk_channel.members:
						self.stop_count(member)
