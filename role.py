# Бот подписчик
from datetime import date
import discord
from discord.ext import commands
import os
from discord.ext.commands import Bot
import asyncio
#API_KEY = "AIzaSyC3qBObRiGZaV1icDbcN3HS7gcbpose6Uk"


prefix = "."
bot = commands.Bot(command_prefix= prefix)

# чат-бот
cn = {'канал','канал рухи','Канал','Канал рухи','ютуб','скинь канал','дай канал рухи','скинь канал рухи сан','дай канал рухи сан'}

# Запуск
@bot.event
async def on_ready():
    game = discord.Game("Mobile SA-MP")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Бот запущен!")

# Команда help
bot.remove_command('help')

@bot.command()
async  def help(ctx):
    emb = discord.Embed(title= "Помощь")

    emb.add_field(name="{}команды".format(prefix), value="Список команд")

    await ctx.send(embed=emb)
# admin help
@bot.command()
@commands.has_permissions(administrator = True)
async  def ahelp(ctx):

    emb = discord.Embed(title= "Админ команды:", colour= discord.Colour.red())

    await ctx.channel.purge(limit=10)

    emb.add_field(name="{}clear".format(prefix), value="Очистить чат",inline=False)
    emb.add_field(name="{}ainfo (ID пользователя)".format(prefix), value="Информация про пользователя",inline=False)
    emb.add_field(name="{}ban (ID пользователя)".format(prefix), value="Забанить",inline=False)
    emb.add_field(name="{}kick (ID пользователя)".format(prefix), value="Кикинуть",inline=False)
    emb.add_field(name="{}mute (ID пользователя)".format(prefix), value="Дать мут",inline=False)

    await ctx.send(embed=emb)
# clear
@bot.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, count=100):
    author = ctx.message.author
    await ctx.channel.purge(limit=count)
    await ctx.send(embed= discord.Embed(description=f'Чат очистил администратор: {author.mention}'))

#@bot.command()
#async def subs(ctx):
 #   author = ctx.message.author
  #  await ctx.send(f"Функция ещё не работает{author.mention}!")

# Чат бот
@bot.command()
async def руха(ctx,arg):
    if arg in cn:
        author = ctx.message.author
        await ctx.send(f"Вот держи братан {author.mention}!\nhttps://www.youtube.com/channel/UC7uCfzRfy2UDVtuxnr3jjBA/videos")


# отключение от канала
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(658746681172688900)
    await channel.send(embed=discord.Embed(description=f'Нас покинул``{member.name}``, Руха растроился :(', color=0x00FF00))

# Подключение к каналу
@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(658746681172688900)
    role = discord.utils.get(member.guild.roles, id=670271810079555584)
    await member.add_roles(role)
    await channel.send(embed= discord.Embed(description=f'Наш новый друг``{member.name}``!',color=0x00FF00))


# commands
@bot.command()
async def команды(ctx):
    emb = discord.Embed(title= "Команды сервера", colour= discord.Colour.red())
    await ctx.channel.purge(limit=10)
    emb.add_field(name= '{}info'.format(prefix), value='Информация о пользователе.',inline=False)
    await ctx.send(embed= emb)
# mute
@bot.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, *,reason=None):
    emb = discord.Embed(title="Выдан мут пользователю", colour=discord.Colour.red())
    ctx.channel.purge(limit=1)
    role = discord.utils.get(member.guild.roles, id=670630763716149248)
    await member.add_roles(role)
    emb.set_author(name= member.name, icon_url=member.avatar_url)
    emb.add_field(name='Пользователь замучен!', value='Замутен {} с причиной {}'.format(member.name,format(reason)))
    emb.set_footer(text= 'Замучен Администратором {}'.format(ctx.author.name), icon_url =ctx.author.avatar_url)
    await ctx.send(embed=emb)

# unmute
@bot.command()
@commands.has_permissions(administrator = True)
async def unmute(ctx, member: discord.Member):
    emb = discord.Embed(title="Пользователь размучен!", colour=discord.Colour.green())
    ctx.channel.purge(limit=1)
    role = discord.utils.get(member.guild.roles, id=670630763716149248)
    await member.remove_roles(role)
    emb.set_author(name= member.name, icon_url=member.avatar_url)
    emb.set_footer(text= 'Мут снят Администратором {}'.format(ctx.author.name), icon_url =ctx.author.avatar_url)
    await ctx.send(embed=emb)

@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *,reason=None):
        emb = discord.Embed(title="Пользователь забанен", colour=discord.Colour.red())
        ctx.channel.purge(limit=1)
        await member.ban(reason=reason)
        emb.set_author(name= member.name, icon_url=member.avatar_url)
        emb.add_field(name='', value='Забанен {} с причиной {}'.format(member.name,format(reason)))
        emb.set_footer(text= 'Забанен Администратором {}'.format(ctx.author.name), icon_url =ctx.author.avatar_url)
        await ctx.send(embed=emb)

#info
@bot.command()
async def info(ctx, user: discord.User):
        emb = discord.Embed(title="Статистика пользователя {}".format(user.name), colour=discord.Colour.red())
        ctx.channel.purge(limit=1)
        emb.set_author(name= user.name, icon_url=user.avatar_url)
        emb.add_field(name=user.name, value='Имя пользователя')
        #emb.add_field(name="Создание профиль дискорда: ", value=str(user.created_at)[:16])
        emb.set_footer(text= 'Смотрит статистику {}'.format(ctx.author.name), icon_url =ctx.author.avatar_url)
        await ctx.send(embed=emb)

#bot.run('')
client = os.environ.get('BOT_TOKEN')