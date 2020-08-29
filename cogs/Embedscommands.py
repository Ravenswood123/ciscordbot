import discord
from discord.ext import commands

class Embedscommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name='embeds', invoke_without_command=True)
	async def embedscmd(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(description = 'Правила однинаковы для всех участников сервера. Соблюдайте их чтобы сделать комфортным общение всех пользователей',colour=0xFFC700)
		emb.set_author(name='Правила', icon_url=self.bot.user.avatar_url)
		emb.add_field(name='**1. Запрещено флудить (_флуд - это одинаковые по смыслу сообщения_)**', value='**``наказание мут 1h + 1 warn``**', inline = False)
		emb.add_field(name='**1.1. Запрещены сообщения не по тематике канала (оффтоп)**',value='**``сообщения просто будут удалены``**', inline=False)
		emb.add_field(name='**1.2 Запрещено распространять NSFW контент в любом контексте (аватарки, сообщения, фото, видео и т.д.)**',value='**``Кроме канала``** <#745590630453084181>**``Наказание: 2 warns``**', inline=False)
		emb.add_field(name='**1.3. Запрещена реклама дискорд серверов, магазинов аккаунтов, различных соц.сетей и сайтов**', value='**``наказание мут 5h + 1 warn``**', inline = False)
		emb.add_field(name='**2. Запрещено использовать SoundPad в открытых комнатах, или если участники комнаты против его использования**',value='**``наказание мут 6h``**', inline=False)
		emb.add_field(name='**2.1. Запрещено кричать открытых комнатах, или если участники комнаты против этого**', value='**``наказание мут 6h``**', inline=False)
		emb.add_field(name='**2.2. Запрещено оскорблять, выводить на конфликт любых участников голосового канала**', value='**``наказание мут 30min``**', inline=False)
		emb.add_field(name='**3. Запрещен слив, распространение личной информации**',value='**``наказание мут 10h + 2 warns``**', inline=False)
		emb.add_field(name='**3.1. Запрещено выпрашивать роли (если вы не выполнили требования для получения той, или иной роли)**',value='**``наказание мут 10h + 1 warn``**', inline=False)
		emb.add_field(name='**5.Модераторы имеют право банить за спорные конфликты**',value='**``то есть, если в спорной ситуации вас забанили, это считается оправданым``**', inline=False)
		emb.add_field(name='**5.1. Последующие наказания**',value='**``при повторных нарушениях правил (5/5) вам даётся мут на неделю, при последующих нарушениях вам будет выдан перманентный бан``**', inline=False)
		await ctx.send(embed=emb)

	#Rules
	@embedscmd.command(name='rules')
	async def rules_subcommand(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(description='**Если вы прочитали правила, то нажмите на галочку снизу для получения доступа к дискорд серверу**',colour=colour=0xFFC700)
		await ctx.send(embed=emb)



	#Welcome
	@embedscmd.command(name='welcome')
	async def welcome_subcommand(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(description='Добро пожаловать на наш сервер. Он создан для объединения снг дизайнеров в одно большое и дружелюбное community. Здесь можно делиться своими работами, соц.сетями с дизайном и т.д. Главная цель сервера - _общение_. Поэтому соблюдайте правила, которые написаны в канале <#738623605251899422> чтобы сделать приятную атмосферу для каждого участника', colour=0xFFC700)
		emb.set_author(name='Добро пожаловать!', icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=emb)
	# Navigation
	@embedscmd.command(name='clans')
	async def clans_subcommand(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(description='**1.** Для создания клана вам нужно иметь 10.000\n**2.** После чего вы должны написать любому человеку с ролью <@&745605489269669999>\n**3.** С вашего счёта спишется 10.000 коинов\n4. Вам будет выдана роль <@&745605823945900102>\n**5.** У вашего клана появится собственная голосовая комната, а также текстовый канал\n**6.** По вопросам или назначениям ролей участникам клана, писать <@&745605489269669999> ',colour=0xFFC700)
		emb.set_author(name='Кланы', icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=emb)

	# Navigation
	@embedscmd.command(name='roles')
	async def roles_subcommand(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(description='<@&745605489269669999>\n **``Им можно написать по вопросам, получением ролей``**\n \n <@&746282842908262454>\n **``Модерирует чат, голосые каналы. Наказывает пользователей, которые не соблюдают ``**<#745197415354597446>\n \n<@&745597993797025813> **``Проводит различные ивенты в канале``** <#746009517170491512>\n \n <@&746006871864770771>\n **``Создатель бота/разработчик. К нему можно обратится по вопросам бота, ошибкам (если что-то не работает)``**\n \n <@&748981430305947701>\n **``Выдаётся за Nitro Boost сервера. Получает доступ создать комнату в соотвутсвуещем канале, выделяется справа. Также получает 5000 коинов на свой счёт``**<@&745619648015368232>\n **``Можно получить за достижение 15.000 на YouTube. Люди с этой ролью получают возможность создать свой канал в соответствующей категории, а также выделяются в списке участников``**\n \n <@&745619537067507773>\n **``Можно получить за достижение 5.000 на YouTube. Люди с этой ролью получают возможность создать свой канал в соответствующей категории, а также выделяются в списке участников``**\n \n <@&745617026726232114>\n **``Можно получить за достижение 2.000 на YouTube``**\n \n <@&745618878826151997>\n **``Можно получить за достижение 15.000 на Twitch. Люди с этой ролью получают возможность создать свой канал в соответствующей категории, а также выделяются в списке участников``**\n \n <@&745618842209746954>\n **``Можно получить за достижение 5.000 на Twitch. Люди с этой ролью получают возможность создать свой канал в соответствующей категории, а также выделяются в списке участников``**\n \n <@&745617098117611562>\n **``Можно получить за достижение 2.000 на Twitch``**\n \n <@&745605823945900102>\n **``Можно получить при создании клана. О кланах написано в``** <#745592786312757248>\n \n <@&745610141382082562>, <@&745610323653820447> <@&746008073704964097>, <@&746008239086501988>, <@&746008294132416512>\n **``Выдается за получение варнов соответствующего количества``** \n \n <@&745621049114099812>, <@&745620967073644625>, <@&745620841177415732>\n **``Выдаётся за соответствующий заработок с внутриигровых турниров Fortnite``**\n \n <@&745608903902887956>\n **``Выдаётся за ознакомление с правилами в канале``**<#745197415354597446>\n \n <@&746007812454481920>\n **``Можно получить при наличии хорошего микрофона``**\n \n <@&746009784502845440>\n **``Выдаётся при включении уведомлений в канале``**<#746009517170491512>',colour=0xFFC700)
		emb.set_author(name='Роли', icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=emb)

	# News
	@embedscmd.command(name='news')
	async def news_subcommand(self, ctx, user_text=None):
		await ctx.message.delete()
		emb = discord.Embed(description=str(user_text),colour=discord.Colour.from_rgb(102, 11, 237))
		emb.set_author(name='Новости', icon_url=self.bot.user.avatar_url)
		emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=emb)

	# Events
	@embedscmd.command(name='events')
	async def events_subcommand(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(description='**Ивенты** - различные мини-игры на сервере.\n В них может принять участие любой желающий. За различные ивенты вы можете получить вознаграждение в виде _коинов_ разного количества.',colour=0xFFC700)
		emb.set_author(name='Ивенты', icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=emb)

	@embedscmd.command(name='eventsnotfy')
	async def eventsnptfy_subcommand(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(description='**Для того, чтобы получать уведомления о различных ивентах, нажмите на реакцию снизу.**\n \nP.s Если вы хотите отключить уведомления, повторно нажмите на реакцию',colour=0xFFC700)
		await ctx.send(embed=emb)
#Add cog files
def setup(bot):
	bot.add_cog(Embedscommands(bot))
