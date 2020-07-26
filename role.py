# Бот подписчик
# Бот подписчик
import discord
from discord.ext import commands
import asyncio
import random
import time
from datetime import datetime
import os


time_string = time.strftime("%A %X")

prefix = "."
bot = commands.Bot(command_prefix=prefix)


# Команда help
bot.remove_command('help')


# clear
@bot.command()
async def clear(ctx, count=20):
    author = ctx.message.author
    await ctx.channel.purge(limit=count)
    await ctx.send(embed=discord.Embed(description=f'✅ Очищено {count} сообщений.'))
    time.sleep(3.0)
    await ctx.channel.purge(limit=1)

# Чат бот
@bot.command()
async def ip(ctx):
        author = ctx.author
        await ctx.send(f"Вот держи {author.mention}! SanTrope #02 - `51.77.32.196:7777`, сервер где играет loveruha, вводи его промокод #LOVERUHA, и получешь свои первые деньги!")



# отключение от канала
@bot.event
async def on_member_remove(user: discord.Member):
    channel = bot.get_channel(687640950931193866)
    emb = discord.Embed(color=discord.Colour.red())
    emb.set_author(name=f' {user.name}#{user.discriminator}, отошел в преисподнюю',icon_url=user.avatar_url)
    await channel.send(embed=emb)
# Подключение к каналу
@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(687640950931193866)
    role = discord.utils.get(member.guild.roles, id=670271810079555584)
    await member.add_roles(role)
    emb = discord.Embed(colour=discord.Colour.orange())
    emb.set_author(name='У нас пополнение!',icon_url=member.avatar_url)
    emb.add_field(name='Welcome!',value='Рады видеть тебя здесь {} 🤚'.format(member.mention),inline=False)
    emb.add_field(name='Информация',value='● Пожалуйста, прочитайте наши `#правила`'
                  '\n● Выберите сервер на котором, вы играете `#сервер`'
                  "\n● Посмотреть новые видео loveruh'i`#news`"
                  "\n● Заходи на канал `#chat` и общайся",inline=False)
    emb.add_field(name='Нужна помощь?',value='Пишите в раздел `#помощь`')
    await channel.send(embed=emb)



# commands
@bot.command()
async def help(ctx):
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title="Помощь по боту", colour=discord.Colour.orange())
        emb.add_field(name='Команды:',value='`.info` - Посмотреть статистику (Упомянуть пользователя - "@")'
                            '\n`.ip` - Сервер где играет loveruha!')
        await ctx.send(embed=emb)



# info
@bot.command()
async def info(ctx, user: discord.Member):
    emb = discord.Embed(title="Статистика `{}`".format(user.name), colour=discord.Colour.blue())
    await ctx.channel.purge(limit=1)
    emb.add_field(name='Имя:', value=user.name)
    emb.add_field(name="Зашёл на канал:", value=str(user.joined_at)[:10])
    emb.add_field(name='ID пользователя:', value=user.id, inline=False)
    emb.set_thumbnail(url=str(user.avatar_url))
    emb.set_footer(text='Смотрит {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@bot.command()
async def kick(ctx, user:discord.Member,*,reason=None):
    author = ctx.author
    role_names = [role.name for role in author.roles]
    if ("Модератор" in role_names):
        channel = bot.get_channel(710559011505700945)
        #ответ модеру
        emb = discord.Embed(colour=discord.Colour.red())
        emb.set_author(name=f'{user.name}#{user.discriminator}  исключен', icon_url=user.avatar_url)
        emb.set_footer(text=f' Модератером {ctx.author.name}')
        await ctx.send(embed=emb)
        #logs
        emb = discord.Embed(colour=discord.Colour.red())
        emb.set_author(name=f'{user.name}#{user.discriminator}  исключен', icon_url=user.avatar_url)
        emb.set_footer(text=f' Модератером {ctx.author.name}')
        await user.kick(reason=reason)
        await channel.send(embed=emb)
    else:
        return
@bot.command()
async def gunban(ctx, user:discord.abc.User):
    channel = bot.get_channel(710559011505700945)
    await user.unban(reason=1)
    emb = discord.Embed(title="`{}` разбанен".format(user.name), colour=discord.Colour.red())
    emb.add_field(name='ID пользователя:', value=user.id)
    emb.add_field(name='Время:', value=time_string)
    emb.set_thumbnail(url=str(user.avatar_url))
    emb.set_footer(text='Наказание снял {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await channel.send(embed=emb)

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user:discord.Member,*,reason=None):
    channel = bot.get_channel(710559011505700945)
    #answer
    emb = discord.Embed(colour=discord.Colour.red())
    emb.set_author(name=f'{user.name}#{user.discriminator} заблокирован', icon_url=user.avatar_url)
    emb.set_footer(text=f' Модератером {ctx.author.name}')
    await ctx.send(embed=emb)
    #log
    emb = discord.Embed(colour=discord.Colour.red())
    emb.set_author(name='Заблокирован', icon_url=user.avatar_url)
    emb.add_field(name="Пользователь", value=f'{user.name}#{user.discriminator}')
    emb.add_field(name='ID', value=user.id)
    emb.add_field(name='Модератор', value=ctx.author.name)
    emb.add_field(name='Причина', value=reason,inline=False)
    await user.ban(reason=reason, delete_message_days=1)
    await channel.send(embed=emb)


@bot.command()
async def mute11(ctx, user:discord.Member,*,time1=120):
    author = ctx.author
    role_names = [role.name for role in author.roles]
    if ("Модератор" in role_names):
        role = discord.utils.get(user.guild.roles, id=710558272846823518)
        channel = bot.get_channel(710559011505700945)
        await user.add_roles(role)
        emb = discord.Embed(title="{} заглушен".format(user.name), colour=discord.Colour.red())
        emb.add_field(name='ID пользователя:', value="{}".format(user.id))
        emb.add_field(name='Длительность:', value='{} минут'.format(int(time1)))
        emb.add_field(name='Модератор', value="{}".format(ctx.author.name),inline=False)
        emb.set_thumbnail(url=str(user.avatar_url))
        emb.set_footer(text='{}'.format(time_string))
        await channel.send(embed=emb)
        time.sleep(time1*60)
        emb = discord.Embed(title="{} заглушка снята".format(user.name), colour=discord.Colour.orange())
        emb.add_field(name='ID пользователя:', value="{}".format(user.id))
        emb.add_field(name='Модератор', value="Auto")
        emb.set_thumbnail(url=str(user.avatar_url))
        emb.set_footer(text='{}'.format(time_string))
        await channel.send(embed=emb)
        await user.remove_roles(role)
    else:
        return
@bot.command()
async def unmute11(ctx,user:discord.Member):
    author = ctx.author
    role_names = [role.name for role in author.roles]
    if ("mute" in role_names):
        if ("Модератор" in role_names):
            channel = bot.get_channel(710559011505700945)
            role = discord.utils.get(user.guild.roles, id=710558272846823518)
            emb = discord.Embed(title="{} заглушка снята".format(user.name), colour=discord.Colour.orange())
            emb.add_field(name='ID пользователя:', value="{}".format(user.id))
            emb.add_field(name='Модератор', value="{}".format(ctx.author.name),inline=False)
            emb.set_thumbnail(url=str(user.avatar_url))
            emb.set_footer(text=time_string)
            await channel.send(embed=emb)
            await user.remove_roles(role)
        else:
            return
    else:
        sendd =f'{author.mention} _**Пользователь не заглушен!**_'
        await ctx.send(sendd)

#rules
@bot.command()
async def rules(ctx):
    emb = discord.Embed(title='Правила поведения в дискорде',colour=discord.Colour.orange())
    emb.description ='● Не нарушайте правила и ведите себя хорошо' \
                     '\n● в ином случае будете наказаны!'
    await ctx.send(embed=emb)
    #
    emb = discord.Embed(title='1. Запрещено',colour=discord.Colour.orange())
    emb.description = "\n● Запрещены оскорбления." \
                      "\n● Запрещена реклама разных ресурсов, каналов, сайтов." \
                      "\n● Запрещена продажа игровой валюты и аккаунтов. " \
                      "\n● Запрещено использовать CAPS LOCK!" \
                      "\n● Запрещен обман."
    await ctx.send(embed=emb)
    emb = discord.Embed(title='2. ❌ NSFW контет ❌',colour=discord.Colour.orange())
    emb.description = "\n● Это строго запрещено во время чата или разговора " \
                      "\n● а также в фотографиях профиля, псевдонимах или любым другим способом."
    await ctx.send(embed=emb)

    emb = discord.Embed(title='3. Использование канала',colour=discord.Colour.orange())
    emb.description = "\n●  Пожалуйста, используйте все каналы соответствующим образом" \
                      "\n● Информация о каждом канале находится в его описании или прикрепленном сообщении."
    emb.set_footer(text='С уважением, Администрация канала.')
    await ctx.send(embed=emb)




reacit = [".ban",".mute11",".kick",".unmute11"]
AntiMat = ["ПИДОР","ХУЙНЯ","ЕБАЛ","СДОХНИ","БЛЯДЬ","ХУЙЛО","ебал","нахуй","пизда","ПИЗДА","хуй"]
AntiLink = ["https://","http://"]
@bot.event
async def on_message(msg):
    author = msg.author
    channel = msg.channel
    role_names = [role.name for role in author.roles]
    if "Модератор" in role_names or "bot" in role_names:
        for i in reacit:
            if i in msg.content:
                await msg.add_reaction('✅')
    else:
        for i in AntiLink:
            if i in msg.content:
                await msg.channel.purge(limit=1)
                message2 = f'{author.mention} _**Ссылки запрещены!**_'
                await channel.send(message2)
                break
        for i in AntiMat:
            if i in msg.content:
                await msg.channel.purge(limit=1)
                message1 = f'{author.mention} _**Не ругайтесь!**_'
                await channel.send(message1)
                break

    await bot.process_commands(msg)
#end

@bot.command(aliases = ['v'])
async def video(ctx,link=None):
	    await ctx.channel.purge(limit=1)
	    ch1 = bot.get_channel(670270944828456971)
	    ch2 = bot.get_channel(658746681172688900)
	    #await ctx.send(embed=discord.Embed(description='У loveruha вышел новый видеоролик! Быстрее залетай, ставь лайк и пиши комментарий, чтобы получить свою заветную соточку рублей. \n'+link + ' @everyone ',colour=discord.Colour.red()))
	    await ch1.send('У **loveruha** вышел новый видеоролик! Быстрее залетай, ставь лайк и пиши комментарий, чтобы получить свою заветную соточку рублей. \n'+link + ' @everyone')
	    await ch2.send('У **loveruha** вышел новый видеоролик! Быстрее залетай, ставь лайк и пиши комментарий, чтобы получить свою заветную соточку рублей. \n'+link + ' @everyone')
@bot.event
async def on_ready():
    game = discord.Game("Помощь [.help] ")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Бот запущен!")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Ready.')
    print('------------')

token = os.environ.get("TOKEN")
bot.run(str(token))
