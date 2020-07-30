import discord
from discord.ext import commands
import asyncio
import random
import time
from datetime import datetime
import os
import sqlite3
import io 
import requests
from PIL import Image, ImageFont, ImageDraw

#bd
db = sqlite3.connect('server1.db')
sql = db.cursor()


time_string = time.strftime("%A %X")

prefix = "."
bot = commands.Bot(command_prefix=prefix)


# Команда help
bot.remove_command('help')

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

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        cash INT,
        server_id INT
    )""")

    sql.execute("""CREATE TABLE IF NOT EXISTS shop (
        role_id INT,
        id INT,
        cost BIGINT
    )""")

    for guild in bot.guilds:
        for member in guild.members:
            if sql.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                sql.execute(f"INSERT INTO users VALUES ('{member}',{member.id},{0},{guild.id})")
                db.commit()
            else:
                pass
    db.commit()
    print('База данных запущена!')  



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
    #загрузка в бд юсеров
    if sql.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES ('{member}',{member.id},{0},{member.guild.id}")
        db.commit()
    else:
        pass

    

# отключение от канала
@bot.event
async def on_member_remove(user: discord.Member):
    channel = bot.get_channel(687640950931193866)
    emb = discord.Embed(color=discord.Colour.red())
    emb.set_author(name=f' {user.name}#{user.discriminator}, отошел в преисподнюю',icon_url=user.avatar_url)
    await channel.send(embed=emb)


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
        await ctx.send(f"Вот держи {author.mention}! SanTrope #02 - `51.77.32.196:7777`, сервер где играет loveruha, вводи его промокод #loveruha, и получешь свои первые деньги!")

# commands
@bot.command()
async def help(ctx):
        await ctx.channel.purge(limit=1)
        emb = discord.Embed(title="Помощь по боту", colour=discord.Colour.orange())
        emb.add_field(name='Команды:',value='`.info` - Посмотреть статистику (Упомянуть пользователя - "@")'
                            '\n`.ip` - Сервер где играет loveruha!'
                            '\n`.balanse` - Узнать свой баланс'
                            '\n`.shop` - Магазин'
                            '\n`.buy-role @Role` - Купить роль')
        await ctx.send(embed=emb)


# info
@bot.command()
async def info(ctx, user: discord.Member):
    emb = discord.Embed(title="Статистика `{}#{}`".format(user.name, user.discriminator), colour=discord.Colour.blue())
    await ctx.channel.purge(limit=1)
    emb.add_field(name='Имя:', value=f'{user.name}')
    emb.add_field(name="Зашёл на канал:", value=str(user.joined_at)[:10])
    emb.add_field(name='ID пользователя:', value=user.id,inline=False)
    emb.add_field(name='Баланс:', value=sql.execute('SELECT cash FROM users WHERE id = {}'.format(user.id)).fetchone()[0], inline=True)
    emb.set_thumbnail(url=str(user.avatar_url))
    emb.set_footer(text='Смотрит {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@bot.command()
async def kick(ctx, user:discord.Member,*,reason=None):
    await ctx.channel.purge(limit=1)
    author = ctx.author
    role_names = [role.name for role in author.roles]
    if ("Модератор" in role_names):
        channel = bot.get_channel(710559011505700945)
        #ответ модеру
        emb = discord.Embed(colour=discord.Colour.red())
        emb.set_author(name=f'{user.name}#{user.discriminator}  исключен', icon_url=user.avatar_url)
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
async def u1nban(ctx, user:discord.User):
    channel = bot.get_channel(710559011505700945)
    await user.unban(reason=1)
    emb = discord.Embed(title="`{}` разбанен".format(user.name), colour=discord.Colour.red())
    emb.add_field(name='ID пользователя:', value=user.id)
    emb.add_field(name='Время:', value=time_string)
    emb.set_thumbnail(url=str(user.avatar_url))
    emb.set_footer(text='Наказание снял {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await channel.send(embed=emb)

@bot.command()
async def ban(ctx, user:discord.Member,*,reason=None):
    await ctx.channel.purge(limit=1)
    author = ctx.author
    channel = bot.get_channel(710559011505700945)
    role_names = [role.name for role in author.roles]
    if ("Модератор" in role_names):
        #answer
        emb = discord.Embed(colour=discord.Colour.red())
        emb.set_author(name=f'{user.name}#{user.discriminator} заблокирован', icon_url=user.avatar_url)
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
    else:
        pass

@bot.command()
async def mute(ctx, member: discord.Member, time1: int, *, reason: str = None):
        author = ctx.author
        role_names = [role.name for role in author.roles]
        if ("Модератор" in role_names):
            emb = discord.Embed(colour=discord.Colour.red())
            emb.set_author(name=f'{member.name}#{member.discriminator}` получил блокировку чата на `{time1}м`', icon_url=member.avatar_url)
            await ctx.send(embed=emb)
            #answr
            role = discord.utils.get(member.guild.roles, id=710558272846823518)
            channel = bot.get_channel(710559011505700945)
            await member.add_roles(role)
            emb = discord.Embed(title="{} заглушен".format(member.name), colour=discord.Colour.red())
            emb.add_field(name='ID пользователя:', value="{}".format(member.id))
            emb.add_field(name='Длительность:', value='{} минут'.format(time1))
            emb.add_field(name='Модератор:', value="{}".format(ctx.author.name),inline=False)
            emb.add_field(name='Причина:', value="{}".format(reason),inline=False)
            emb.set_thumbnail(url=str(member.avatar_url))
            emb.set_footer(text='{}'.format(time_string))
            await channel.send(embed=emb)
            await asyncio.sleep(time1*60)
            emb = discord.Embed(title="{} заглушка снята".format(member.name), colour=discord.Colour.orange())
            emb.add_field(name='ID пользователя:', value="{}".format(member.id))
            emb.add_field(name='Модератор:', value="Auto")
            emb.set_thumbnail(url=str(member.avatar_url))
            emb.set_footer(text='{}'.format(time_string))
            await channel.send(embed=emb)
            await member.remove_roles(role)
        else:
            pass
@bot.command()
async def unmute(ctx,user:discord.Member):
    await ctx.channel.purge(limit=1)
    author = ctx.author
    role_names = [role.name for role in author.roles]
    if ("mute" in role_names):
        if ("Модератор" in role_names):
            emb = discord.Embed(colour=discord.Colour.red())
            emb.set_author(name=f'{user.name}#{user.discriminator} блокировка чата снята', icon_url=user.avatar_url)
            await ctx.send(embed=emb)
            #answer
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
            pass
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




AntiMat = ["ПИДОР","ХУЙНЯ","ЕБАЛ","СДОХНИ","БЛЯДЬ","ХУЙЛО","ебал","нахуй","пизда","ПИЗДА","хуй"]
alfa = ['а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я'
        'a','b','c','d','e','f','g','h','o','p','q','r','s','t','u','v','w','x','y','z','.','!','A','B','C','D','E','F','G','H','I','J','K'
        'L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0','-','=','+','~',',','<','>','_'
        'А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я','@','#','$','%','^','&','*','(',')','?',':','№']
AntiLink = ["https://","http://"]
@bot.event
async def on_message(msg):

    for i in alfa:
        if i in msg.content:
            sql.execute("UPDATE users SET cash = cash + {} WHERE id  = {}".format(1, msg.author.id))
            db.commit()   


    author = msg.author
    channel1 = msg.channel
    role_names = [role.name for role in author.roles]

    if "Модератор" in role_names or "bot" in role_names or "Спонсор" in role_names:
        for i in AntiLink:
            if i in msg.content:
                await msg.channel.purge(limit=1)
                message2 = f'{author.mention} _**Ссылки запрещены!**_'
                await channel1.send(message2)
                break
        for i in AntiMat:
            if i in msg.content:
                await msg.channel.purge(limit=1)
                message1 = f'{author.mention} _**Не ругайтесь!**_'
                await channel1.send(message1)
                break
    await bot.process_commands(msg)
#end

@bot.command(aliases = ['v'])
async def __video(ctx,link=None):
        await ctx.channel.purge(limit=1)
        ch1 = bot.get_channel(670270944828456971)
        ch2 = bot.get_channel(658746681172688900)
        ch3 = bot.get_channel(738434306858418229)
        ch4 = bot.get_channel(672171909466685471)
        #await ctx.send(embed=discord.Embed(description='У loveruha вышел новый видеоролик! Быстрее залетай, ставь лайк и пиши комментарий, чтобы получить свою заветную соточку рублей. \n'+link + ' @everyone ',colour=discord.Colour.red()))
        await ch1.send('У **loveruha** вышел новый видеоролик! Быстрее залетай, ставь лайк и пиши комментарий, чтобы получить свою заветную соточку рублей. \n'+link + ' @everyone')
        await ch2.send('У **loveruha** вышел новый видеоролик! Быстрее залетай, ставь лайк и пиши комментарий, чтобы получить свою заветную соточку рублей. \n'+link + ' @everyone')
        await ch3.send('У **loveruha** вышел новый видеоролик! Быстрее залетай, ставь лайк и пиши комментарий, чтобы получить свою заветную соточку рублей. \n'+link + ' @everyone')
        await ch3.send('У **loveruha** вышел новый видеоролик! Быстрее залетай, ставь лайк и пиши комментарий, чтобы получить свою заветную соточку рублей. \n'+link + ' @everyone')
@bot.command()
async def balanse(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed= discord.Embed(description= f"Количество баланса **{ctx.author}** составляет **{sql.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]} :moneybag:**",colour=discord.Colour.blue()))
    else:
        await ctx.send(embed= discord.Embed(description= f"Количество баланса **{member}** составляет **{sql.execute('SELECT cash FROM users WHERE id = {}'.format(member.id)).fetchone()[0]} :moneybag:**",colour=discord.Colour.blue()))
        
@bot.command(aliases= ['+b'])
@commands.has_permissions(administrator=True)
async def __b(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        await ctx.send(f'**{ctx.author}**, укажите пользователя, которому желаете выдать баланс')
    else:
        if amount is None:
            await ctx.send(f'**{ctx.author}**, укажите количество, которые хотите добавить пользователю')
        elif amount < 1:
            await ctx.send(f"**ctx.author**, укажите сумму больше 1")
        else:
            sql.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))    
            db.commit()

            await ctx.message.add_reaction('✅')

@bot.command(aliases= ['-b'])
@commands.has_permissions(administrator=True)
async def __take(ctx, member:discord.Member = None, amount=None):
    if member is None:
        await ctx.send(f'**{ctx.author}**, укажите пользователя, у которого желаете забрать баланс')
    else:
        if amount is None:
            await ctx.send(f'**{ctx.author}**, укажите количество, которые хотите забрать')
        elif amount == 'all':
            sql.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))  
            db.commit() 

        elif int(amount) < 1:
            await ctx.send(f"**ctx.author**, укажите сумму больше 1")
        else:
            sql.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))   
            db.commit()

            await ctx.message.add_reaction('✅')

@bot.command(aliases= ['leaderboard','lb','top'])
async def __leaderboard(ctx):
    embed= discord.Embed(title = 'Топ 5 богачей сервера:',colour=discord.Colour.blue())
    counter = 0
    for row in sql.execute("SELECT name,cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 5".format(ctx.guild.id)):
        counter += 1
        embed.add_field(
            name = f'# {counter} | `{row[0]}`',
            value = f'Баланс: {row[1]}',inline=False
        )
    await ctx.send(embed=embed) 

@bot.command(aliases= ['add-shop'])
async def __add_shop(ctx, role:discord.Role = None, cost: int = None):
    if role is None:
        await ctx.send(f'**{ctx.author}**, укажите роль, которую желаете добавить в магазин')
    else:
        if cost is None:
            await ctx.send(f'**{ctx.author}**, укажите стоимость для роли')
        elif cost < 0:
            await ctx.send(f"**{ctx.author}**, стоимость роли не может быть такой маленькой")
        else:
            sql.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))  
            db.commit()

            await ctx.message.add_reaction('✅')

@bot.command(aliases= ['remove-shop'])
async def __remove_shop(ctx, role:discord.Role = None):
    if role is None:
        await ctx.send(f'**{ctx.author}**, укажите роль, которую желаете удалить в магазине')
    else:
        sql.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))  
        db.commit()

    await ctx.message.add_reaction('✅')

@bot.command(aliases= ['shop'])
async def __shop(ctx):
    emb = discord.Embed(title="Магазин ролей")

    for row in sql.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
        if ctx.guild.get_role(row[0]) != None:
            emb.add_field(
                name= f'Стоимость: {row[1]} :moneybag:',
                value =f'Вы получите роль{ctx.guild.get_role(row[0]).mention}',
                inline=False
            )
        else:
            pass
    await ctx.send(embed = emb)
    await ctx.message.add_reaction('✅')

@bot.command(aliases= ['buy-role'])
async def __buy_role(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f'**{ctx.author}**, укажите роль, которую желаете приобрести')
    else:
        if role in ctx.author.roles:
            await ctx.send(f'**{ctx.author}**, у вас уже имеется данная роль!')
        elif sql.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > sql.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
            await ctx.send(f'**{ctx.author}**, у вас недостаточно средств покупки')
        else:
            await ctx.author.add_roles(role)
            sql.execute('UPDATE users SET cash = cash - {0} WHERE id = {1}'.format(sql.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
            db.commit()
    await ctx.message.add_reaction('✅')

@bot.command()
async def stats(ctx, member:discord.Member=None):
    await ctx.channel.purge(limit=1)
    if member is None:
        img = Image.new('RGBA', (400, 130), '#232529')
        url = str(ctx.author.avatar_url)[:-10]

        response = requests.get(url, stream = True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((100, 100), Image.ANTIALIAS)

        img.paste(response, (15, 15, 115, 115))

        idraw = ImageDraw.Draw(img)
        name = ctx.author.name
        tag = ctx.author.discriminator

        headline = ImageFont.truetype('arial.ttf', size=20)
        undertext = ImageFont.truetype('arial.ttf', size=12)

        idraw.text((145,15), f'{name}#{tag}', font=headline )
        idraw.text((145,50), f'ID: {ctx.author.id}',font= undertext)
        idraw.text((145,70), f'Баланс: {sql.execute("""SELECT cash FROM users WHERE id = {}""".format(ctx.author.id)).fetchone()[0]}',font= undertext)
        img.save('user_card.png')
        await ctx.send(file =discord.File(fp = "user_card.png"))
    else:
        img = Image.new('RGBA', (400, 130), '#232529')
        url = str(member.avatar_url)[:-10]

        response = requests.get(url, stream = True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((100, 100), Image.ANTIALIAS)

        img.paste(response, (15, 15, 115, 115))

        idraw = ImageDraw.Draw(img)
        name = member.name
        tag = member.discriminator

        headline = ImageFont.truetype('arial.ttf', size=20)
        undertext = ImageFont.truetype('arial.ttf', size=12)

        idraw.text((145,15), f'{name}#{tag}', font=headline )
        idraw.text((145,50), f'ID: {member.id}',font= undertext)
        idraw.text((145,70), f'Баланс: {sql.execute("""SELECT cash FROM users WHERE id = {}""".format(member.id)).fetchone()[0]}',font= undertext)
        img.save('user_card.png')
        await ctx.send(file =discord.File(fp = "user_card.png"))

token = os.environ.get("TOKEN")
bot.run(str(token))
