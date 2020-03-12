# Бот подписчик
import discord
from discord.ext import commands
import time
import os



named_tuple=time.localtime()
time_string=time.strftime("%d.%m.%Y - %H:%M", named_tuple)

prefix="."
bot=commands.Bot(command_prefix=prefix)

# main chat

# чат-бот
cr={'канал', 'канал рухи', 'Канал', 'Канал рухи', 'ютуб', 'скинь канал', 'дай канал рухи', 'скинь канал рухи сан',
    'дай канал рухи сан'}

cn=['канал', 'привет']


# Запуск
@bot.event
async def on_ready():
    game=discord.Game("Mobile SA-MP")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Бот запущен!")


# Команда help
bot.remove_command('help')


@bot.command()
async def help(ctx):
    emb=discord.Embed(title="Помощь", colour=discord.Colour.orange())

    emb.add_field(name="{}comm".format(prefix), value="Список команд")

    await ctx.send(embed=emb)


# admin help
@bot.command()
@commands.has_permissions(administrator=True)
async def ahelp(ctx):
        emb=discord.Embed(title="Админ команды:", colour=discord.Colour.orange())
        await ctx.channel.purge(limit=1)
        emb.add_field(name="Очистить чат", value="{}clear либо .clear (число - сколько удалить сообщений)".format(prefix),inline=False)
        emb.add_field(name="Дать мут", value="{}mute [Упомянуть пользователя - '@'] [причина мута]".format(prefix),inline=False)
        emb.add_field(name="Снять мут", value="{}unmute [Упомянуть пользователя - '@']".format(prefix), inline=False)
        emb.add_field(name="Админ команды:", value="{}ahelp".format(prefix), inline=False)
        emb.add_field(name="Информация про пользователя", value="{}ainfo (Упомянуть пользователя - '@')".format(prefix),inline=False)
        emb.add_field(name="Забанить", value="{}ban [Упомянуть пользователя - '@'] [причина бана]".format(prefix),inline=False)
        emb.add_field(name="Разбанить", value="{}unban [Упомянуть пользователя - '@'] (в разработке)".format(prefix),inline=False)
        emb.add_field(name="Кикинуть", value="{}kick [Упомянуть пользователя - '@'] [причина кика]".format(prefix),inline=False)
        await ctx.send(embed=emb)




# clear
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, count=20):
    author=ctx.message.author
    await ctx.channel.purge(limit=count)
    await ctx.send(embed=discord.Embed(description=f'Чат очистил администратор: {author.mention}'))


# @bot.command()
# async def subs(ctx):
#   author = ctx.message.author
#  await ctx.send(f"Функция ещё не работает{author.mention}!")

# Чат бот
@bot.command()
async def ruha(ctx, arg):
    author=ctx.message.author
    for i in cn:
        if i in arg:
            await ctx.send(
                f"Вот держи братан {author.mention}!\nhttps://www.youtube.com/channel/UC7uCfzRfy2UDVtuxnr3jjBA/videos")
        else:
            await ctx.send(f'Я тебя не понимаю!{author.mention}')


# отключение от канала
@bot.event
async def on_member_remove(user: discord.Member):
    channel=bot.get_channel(687640950931193866)
    if on_member_remove == user.kick or on_member_remove == user.ban:
        await channel.send(embed=discord.Embed(description=f'Нас покинул``{user.name}``, Руха растроился :(',
                                               color=discord.Colour.red()))


# Подключение к каналу
@bot.event
async def on_member_join(member: discord.Member):
    channel=bot.get_channel(687640950931193866)
    role=discord.utils.get(member.guild.roles, id=670271810079555584)
    await member.add_roles(role)
    await channel.send(embed=discord.Embed(
        description=f"Приветствую {member.name},ты зашел на Discord сервер Ruh'и!", color=discord.Colour.green()))


# commands
@bot.command()
async def comm(ctx):
    emb=discord.Embed(title="Команды ботов", colour=discord.Colour.orange())
    await ctx.channel.purge(limit=1)
    emb.add_field(name='Руха БОТ\nИнформация о пользователе:',
                  value='{}info (Упомянуть пользователя - "@")'.format(prefix), inline=False)
    emb.add_field(name='Музыкальный бот:',
                  value='!play [название], !stop (остановить), !play (продолжить), !help (подробно о БОТе)'
                        '!skip (пропустить), !join (пригласить бота), !clear(очистить плейлист) !disconnect (отключить бота)',inline=False)
    # emb.add_field(name='Поговорить с ботом.', value='.ruha [text]', inline=False)
    await ctx.send(embed=emb)


# mute
@bot.command()
async def mute(ctx, user: discord.Member, reason=None):
    author=ctx.message.author
    role_names=[role.name for role in author.roles]
    if "Хелпер" in role_names:
        emb=discord.Embed(title="Выдан мут пользователю!", colour=discord.Colour.red())
        await ctx.channel.purge(limit=1)
        role=discord.utils.get(user.guild.roles, id=670630763716149248)
        await user.add_roles(role)
        emb.set_author(name=user.name, icon_url=user.avatar_url)
        emb.add_field(name='Имя:', value=user.name)
        emb.add_field(name='ID пользователя:', value=user.id)
        emb.add_field(name='Причина:', value=reason, inline=False)
        emb.add_field(name='Дата и время:', value=time_string, inline=False)
        emb.set_footer(text='Замучен Администратором {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    else:
        author=ctx.message.author
        await ctx.send(f'{author.mention} У тебя недостаточно прав!')


# unmute
@bot.command()
async def unmute(ctx, user: discord.Member):
    author=ctx.message.author
    role_names=[role.name for role in author.roles]
    if "Хелпер" in role_names:
        emb=discord.Embed(title="Пользователь размучен!", colour=discord.Colour.green())
        await ctx.channel.purge(limit=1)
        role=discord.utils.get(user.guild.roles, id=670630763716149248)
        await user.remove_roles(role)
        emb.set_author(name=user.name, icon_url=user.avatar_url)
        emb.set_footer(text='Мут снят Администратором {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    else:
        author=ctx.message.author
        await ctx.send(f'{author.mention} У тебя недостаточно прав!')


# ban
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    emb=discord.Embed(title="Пользователь забанен", colour=discord.Colour.red())
    await ctx.channel.purge(limit=1)
    await user.ban(reason=reason)
    emb.set_author(name=user.name, icon_url=user.avatar_url)
    emb.add_field(name='Имя:', value=user.name)
    emb.add_field(name='ID пользователя:', value=user.id)
    emb.add_field(name='Причина:', value=reason, inline=False)
    emb.add_field(name='Дата и время:', value=time_string)
    emb.set_footer(text='Забанен Администратором {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


# unban
@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx):
    author=ctx.message.author
    ctx.send(f'Команда в разработке!{author.mention}')


# kick

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, user: discord.Member, reason=None):
    emb=discord.Embed(title='Пользаватель кикнут!', colour=discord.Colour.red())
    await ctx.channel.purge(limit=1)
    emb.set_author(name=user.name, icon_url=user.avatar_url)
    emb.add_field(name='Имя:', value=user.name)
    await user.kick(reason=reason)
    emb.add_field(name='ID пользователя:', value=user.id)
    emb.add_field(name='Причина:', value=reason, inline=False)
    emb.add_field(name='Дата и время:', value=time_string)
    emb.set_footer(text='Кикнут Администратором {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


# info
@bot.command()
async def info(ctx, user: discord.Member):
    emb=discord.Embed(title="Статистика пользователя:", colour=discord.Colour.blue())
    await ctx.channel.purge(limit=1)
    emb.set_author(name=user.name)
    emb.add_field(name='Имя:', value=user.name)
    emb.add_field(name="Зашёл на канал:", value=str(user.joined_at)[:10])
    emb.add_field(name='Статус:', value=user.status)
    emb.add_field(name='ID пользователя:', value=user.id, inline=False)
    emb.set_thumbnail(url=str(user.avatar_url))
    emb.set_footer(text='Смотрит {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@bot.command()
async def ainfo(ctx, user: discord.Member):
    author=ctx.message.author
    role_names=[role.name for role in author.roles]
    if "Хелпер" in role_names:
        emb=discord.Embed(title="Статистика пользователя:", colour=discord.Colour.blurple())
        await ctx.channel.purge(limit=1)
        emb.set_author(name=user.name)
        emb.add_field(name='Имя:', value=user.name)
        emb.add_field(name="Зашёл на канал:", value=str(user.joined_at)[:10])
        emb.add_field(name='Статус:', value=user.status)
        emb.add_field(name='ID пользователя:', value=user.id, inline=False)
        emb.add_field(name="Аккаунт создан:", value=str(user.created_at)[:10])
        role=discord.utils.get(user.guild.roles, id=670630763716149248)
        if role in user.roles:
            emb.add_field(name='Заглушка:', value='Есть')
        else:
            emb.add_field(name='Заглушка:', value='Нету')
        emb.set_thumbnail(url=str(user.avatar_url))
        emb.add_field(name='Играет в:', value=user.activity)
        emb.set_footer(text='Смотрит {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    else:
        author=ctx.message.author
        await ctx.send(f'{author.mention} У тебя недостаточно прав!')


        
token = os.environ.get("TOKEN")
bot.run(str(token))


