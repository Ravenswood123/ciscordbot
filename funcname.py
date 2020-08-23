def start_count(self, member: discord.Member)mongo_token=os.environ.get('MONGO_TOKEN'):
	cluster = MongoClient(mongo_token)
	db = cluster["ciscord"]
	collection = db[f"{member.guild.name}"]
	time_now = datetime.datetime.now(tz=None).strftime("%d-%m-%Y %H:%M:%S")
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
	time_now = datetime.datetime.now(tz=None)
	time_in_voice_hrs = time_now.hour - time_join.hour
	time_in_voice_hrs = time_in_voice_hrs * 60
	time_in_voice_minute = time_now.minute - time_join.minute
	time_in_voice_all = time_in_voice_minute + time_in_voice_hrs
	minvoice = collection.find_one({"id": int(member.id)})
	minvoice = minvoice["minvoice"]
	minvoice = minvoice + time_in_voice_all
	#coins before
	coins = collection.find_one({"id": member.id})
	coins = coins["coins"]
	coins = coins + time_in_voice_all
	print(time_in_voice_all)
	collection.update_one({"id": member.id}, {"$set": {"coins": coins, "minvoice": minvoice}})
	collection.update_one({"id": member.id}, {"$set": {"time": "NO INFO"}})
	print("db updated")
	return
