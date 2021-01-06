
import discord
from discord.ext import commands
import asyncio
import random
import os
import sqlite3
import io 
import requests




bot = commands.Bot(command_prefix='!!!')


# Команда help
@bot.remove_command('help')

@bot.event
async def on_ready():
	game = discord.Game("Anarchy")
	await bot.change_presence(status=discord.Status.online, activity=game)
	print("Бот запущен!")


@bot.event
async def on_message(msg):
	author = msg.author
	AntiLink = ["https://","http://"]
	channel1 = msg.channel
	role_names = [role.name for role in msg.author.roles]
	if "Leader" in role_names or "Founder" in role_names or "Co-Leader" in role_names or "Admin" in role_names or "Moderator" in role_names:
		pass
	else:
		for i in AntiLink:
			if i in msg.content:
				await msg.channel.purge(limit=1)
				message2 = '{} _**Ссылки запрещены!**_ // _**Links are not allowed!**_'.format(author.mention)
				await channel1.send(message2)
				await asyncio.sleep(3)
				await channel1.purge(limit=1)
				h1 = bot.get_channel(790234910509367317)
				await h1.send(embed=discord.Embed(description='**Пользователь** '+ str(author) +' пытался вставить ссылку!!!\n **Сообщение:** '+str(msg.content),colour=discord.Colour.red()))
			else:
				pass
token = os.environ.get("TOKEN")
bot.run(str(token))
