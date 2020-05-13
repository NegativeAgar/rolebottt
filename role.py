# Бот подписчик
import discord
from discord.ext import commands
import asyncio
import random
import time
import os

named_tuple = time.localtime()
time_string = time.strftime("%d.%m.%Y - %H:%M", named_tuple)

prefix = "."
bot = commands.Bot(command_prefix=prefix)


# Команда help
bot.remove_command('help')


# clear
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, count=20):
    author = ctx.message.author
    await ctx.channel.purge(limit=count)
    await ctx.send(embed=discord.Embed(description=f'Чат очистил администратор: {author.mention}'))
    time.sleep(3.0)
    await ctx.channel.purge(limit=1)

# Чат бот
@bot.command()
async def ip(ctx):
    author = ctx.message.author
    await ctx.send(f"Вот держи {author.mention}! SanTrope #02 - `51.83.146.10:8888`, сервер где играет Руха, скорее залетай к нему!")

# отключение от канала
@bot.event
async def on_member_remove(user: discord.Member):
    channel = bot.get_channel(687640950931193866)
    await channel.send(embed=discord.Embed(description=f'Нас покинул `{user.name}`, Руха растроился :(',
                                               color=discord.Colour.red()))


# Подключение к каналу
@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(687640950931193866)
    role = discord.utils.get(member.guild.roles, id=670271810079555584)
    await member.add_roles(role)
    emb = discord.Embed(title="Приветствуем тебя на Discrod сервере Ruh'i", colour=discord.Colour.orange())
    emb.add_field(name='Welcom!',value='Рады видеть тебя здесь {} 🤚'.format(member.mention),inline=False)
    emb.add_field(name='Информация',value='● Пожалуйста, прочитайте наши `#правила`'
                  '\n● Выберите сервер на котором, вы играете `#сервер`'
                  "\n● Посмотреть новое видео Ruh'i `#новые-ролики`",inline=False)
    emb.add_field(name='Нужна помощь?',value='Пишите в раздел `#помощь`')
    await channel.send(embed=emb)
    #await channel.send(embed=discord.Embed(description=f"Приветствую {member.name},ты зашел на Discord сервер Ruh'и!"





# commands
@bot.command()
async def help(ctx):
    emb = discord.Embed(title="Помощь по боту", colour=discord.Colour.orange())
    await ctx.channel.purge(limit=1)
    emb.add_field(name='Команды:',value='`.info` - Посмотреть статистику (Упомянуть пользователя - "@")'
                        '\n`.ip` - Сервер где играет Руха!', inline=False)
    await ctx.send(embed=emb)

emoji = '✅'


# ban
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user: discord.Member):
    author = ctx.message.author
    #await ctx.channel.purge(limit=1)
    await user.ban(reason=1)
    await author.add_reaction(":zap:")


# kick

@bot.command()
async def kick(ctx, user: discord.Member, reason=None):
    author = ctx.message.author
    role_names = [role.name for role in author.roles]
    if "Хелпер" in role_names:
        emb = discord.Embed(title='Пользаватель кикнут!', colour=discord.Colour.red())
        await ctx.channel.purge(limit=1)
        emb.set_author(name=user.name, icon_url=user.avatar_url)
        emb.add_field(name='Имя:', value=user.name)
        await user.kick(reason=reason)
        emb.add_field(name='ID пользователя:', value=user.id)
        emb.add_field(name='Причина:', value=reason, inline=False)
        emb.add_field(name='Дата и время:', value=time_string)
        emb.set_footer(text='Кикнут Администратором {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    else:
        author = ctx.message.author
        await ctx.send(f'{author.mention} У тебя недостаточно прав!')

# info
@bot.command()
async def info(ctx, user: discord.Member):
    emb = discord.Embed(title="Статистика пользователя:", colour=discord.Colour.blue())
    await ctx.channel.purge(limit=1)
    emb.set_author(name=user.name)
    emb.add_field(name='Имя:', value=user.name)
    emb.add_field(name="Зашёл на канал:", value=str(user.joined_at)[:10])
    emb.add_field(name='Статус:', value=user.status)
    emb.add_field(name='ID пользователя:', value=user.id, inline=False)
    emb.set_thumbnail(url=str(user.avatar_url))
    emb.set_footer(text='Смотрит {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)




@bot.event
async def on_ready():
    game = discord.Game("SA-MP Mobile")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Бот запущен!")

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Ready.')
    print('------------')

token = os.environ.get("TOKEN")
bot.run(str(token))

