# Бот подписчик
from datetime import date
import discord
from discord.ext import commands
import time
import config
import os

#API_KEY = "AIzaSyC3qBObRiGZaV1icDbcN3HS7gcbpose6Uk"
named_tuple = time.localtime()
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

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
    emb = discord.Embed(title= "Помощь",colour= discord.Colour.orange())

    emb.add_field(name="{}команды".format(prefix), value="Список команд")

    await ctx.send(embed=emb)
# admin help
@bot.command()
@commands.has_permissions(administrator = True)
async  def ahelp(ctx):

    emb = discord.Embed(title= "Админ команды:", colour= discord.Colour.orange())

    await ctx.channel.purge(limit=10)

    emb.add_field(name="Очистить чат", value="{}clear".format(prefix),inline=False)
    emb.add_field(name="Информация про пользователя", value="{}ainfo (ID пользователя)".format(prefix),inline=False)
    emb.add_field(name="Забанить", value="{}ban [ID пользователя] [причина бана]".format(prefix),inline=False)
    emb.add_field(name="Разбанить", value="{}unban [ID пользователя]".format(prefix),inline=False)
    emb.add_field(name="Кикинуть", value="{}kick [ID пользователя] [причина кика]".format(prefix),inline=False)
    emb.add_field(name="Дать мут", value="{}mute [ID пользователя] [причина мута]".format(prefix),inline=False)
    emb.add_field(name="Снять мут", value="{}unmute [ID пользователя]".format(prefix),inline=False)
    emb.add_field(name="Админ команды:", value="{}ahelp".format(prefix),inline=False)

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
        author = ctx.message.author
        if arg in cn:
            await ctx.send(f"Вот держи братан {author.mention}!\nhttps://www.youtube.com/channel/UC7uCfzRfy2UDVtuxnr3jjBA/videos")
        else:
            await  ctx.send(f'Я тебя не понимаю!{author.mention}')

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
    emb = discord.Embed(title= "Команды ботов", colour= discord.Colour.orange())
    await ctx.channel.purge(limit=10)
    emb.add_field(name= 'Информация о пользователе.', value='{}info'.format(prefix),inline=False)
    emb.add_field(name='Поговорить с ботом.', value='.руха [text]', inline=False)
    await ctx.send(embed= emb)
# mute
@bot.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, *,reason=None):
    emb = discord.Embed(title="Выдан мут пользователю!", colour=discord.Colour.red())
    await ctx.channel.purge(limit=1)
    role = discord.utils.get(member.guild.roles, id=670630763716149248)
    await member.add_roles(role)
    emb.set_author(name= member.name, icon_url=member.avatar_url)
    emb.add_field(name='Имя:', value=member.name)
    emb.add_field(name='ID пользователя:', value=member.id)
    emb.add_field(name='Причина:', value=reason, inline=False)
    emb.add_field(name='Время:', value=time_string,inline=False)
    emb.set_footer(text= 'Замучен Администратором {}'.format(ctx.author.name), icon_url =ctx.author.avatar_url)
    await ctx.send(embed=emb)

# unmute
@bot.command()
@commands.has_permissions(administrator = True)
async def unmute(ctx, member: discord.Member):
    emb = discord.Embed(title="Пользователь размучен!", colour=discord.Colour.green())
    await ctx.channel.purge(limit=1)
    role = discord.utils.get(member.guild.roles, id=670630763716149248)
    await member.remove_roles(role)
    emb.set_author(name= member.name, icon_url=member.avatar_url)
    emb.set_footer(text= 'Мут снят Администратором {}'.format(ctx.author.name), icon_url =ctx.author.avatar_url)
    await ctx.send(embed=emb)
# ban
@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *,reason=None):
        emb = discord.Embed(title="Пользователь забанен", colour=discord.Colour.red())
        await ctx.channel.purge(limit=1)
        await member.ban(reason=reason)
        emb.set_author(name= member.name, icon_url=member.avatar_url)
        emb.add_field(name='Имя:', value=member.name)
        emb.add_field(name='ID пользователя:', value=member.id)
        emb.add_field(name='Причина:', value=reason,inline=False)
        emb.add_field(name='Время:', value=time_string)
        emb.set_footer(text= 'Забанен Администратором {}'.format(ctx.author.name), icon_url =ctx.author.avatar_url)
        await ctx.send(embed=emb)

#unban
@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx):
    ctx.send('Команда в разработке!')

#kick
@bot.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member,reason=None):
    emb = discord.Embed(title='Пользаватель кикнут!', colour=discord.Colour.red())
    await ctx.channel.purge(limit=1)
    emb.set_author(name= member.name, icon_url=member.avatar_url)
    emb.add_field(name='Имя::', value=member.name)
    await member.kick(reason=reason)
    emb.add_field(name='ID пользователя:', value=member.id)
    emb.add_field(name='Причина:', value=reason,inline=False)
    emb.add_field(name='Время:', value=time_string)
    emb.set_footer(text= 'Кикнут Администратором {}'.format(ctx.author.name), icon_url =ctx.author.avatar_url)
    await ctx.send(embed=emb)
#info
@bot.command()
async def info(ctx,user: discord.User):
    emb = discord.Embed(title="Статистика пользователя {}".format(user.name), colour=discord.Colour.blue())
    await ctx.channel.purge(limit=1)
    emb.set_author(name= user.name, icon_url=user.avatar_url)
    emb.add_field(name='Имя пользователя:', value=user.name)
    emb.add_field(name="Создание профиля дискорда: ", value=str(user.created_at)[:16])
    emb.add_field(name='ID пользователя:', value=user.id,inline=False)
    emb.set_footer(text= 'Смотрит статистику {}'.format(ctx.author.name), icon_url =ctx.author.avatar_url)
    await ctx.send(embed=emb)
token = os.environ("TOKEN")
bot.run(token)

