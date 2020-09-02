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
			time_in_voice_all = time_in_voice_minute + time_in_voice_hrs #Time in voice == munutes
		else:
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
				if vc.id != 745611324360228887: #Checking if channel != afk
					for member in vc.members:
						print(member.self_mute)
						if before.channel is None: #Checking for user joined
							if len(after.channel.members) - 1 > 2: #Checking if members before changes were biggest two
								count_status = self.get_stats(member)
								count_status = count_status["count_status"] #Getting count status
								if count_status == "stop": #Checkking status for stop, so as not to start counting already users in channel before
									self.start_count(member) #Stating count
			
							elif len(after.channel.members) >= 2: #Checking if members before changes were smallest two
								for member in after.channel.members: #Checking all members in vc channel
									count_status = self.get_stats(member)
									count_status = count_status["count_status"] #Getting count status
									if count_status == "stop": #Checking for count not started
										print("count started for many members")
										self.start_count(member) #Starting count

						elif after.channel is None: #Checking for user leaved
							if len(before.channel.members) - 1 > 2: #Checking for members after leaved be biggest two
								count_status = self.get_stats(member)
								count_status = count_status["count_status"] #Getting count status
								if count_status == "start": #Checking for count not stopped
									print("count stoped for 1 member")
									self.stop_count(member) #Stopping count

							elif len(before.channel.members) - 1 < 2: #Checking for members after user leaved be smallest two
								for member in before.channel.members: #Checking all members in vc channel
									count_status = self.get_stats(member)
									count_status = count_status["count_status"]
									if count_status == "start": #Checking for count not stopped
										self.stop_count(member) #Stopping count
										
								count_status = self.get_stats(member)
								count_status = count_status["count_status"] #Getting count status
								if count_status == "start": #Checking for count not stopped
									self.stop_count(member) #Stopping count for leaved member
				else:
					channel = discord.utils.get(guild.voice_channels, name='⡇🔕AFK') #Getting afk channel object
					for member in channel.members:
						count_status = self.get_stats(member)
						count_status = count_status["count_status"] #Getting count status
						if count_status == "start": #Checking for count not stopped
							self.stop_count(member) #Stopping coint for afk members
									
def setup(bot):
	bot.add_cog(VoiceCount(bot))
