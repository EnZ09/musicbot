import os
import shutil
from doctest import master
from os import system
import math
import random

import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get


BOT_PREFIX = '!'

bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print("Вход выполнен: " + bot.user.name + "\n")


@bot.command(pass_context=True, aliases=['j', 'joi'])
async def вход(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Бот подключился: {channel}\n")

    await ctx.send(f"Зашёл {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def выход(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Бот покинул нас {channel}")
        await ctx.send(f"Вышел {channel}")
    else:
        print("Бот покинул канал")
        await ctx.send("Меня нету")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def плей(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("Очередь пустая\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Следущмй песня в списке\n")
                print(f"Очередь: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 1

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("Больше песен в очереди нет...\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Удалена старая песня")
    except PermissionError:
        print("Песня воспроизводится")
        await ctx.send("ERROR: Песня играет")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Удалена старая папка очереди")
            shutil.rmtree(Queue_folder)
    except:
        print("Нет старой папки с очередью")

    await ctx.send("Загрузка...")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Играет: {nname[0]}")
    print("Играет\n")


@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def пауза(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Пауза")
        voice.pause()
        await ctx.send("Пауза")
    else:
        print("Не удалось поставить паузу")
        await ctx.send("Не удалось поставить паузу")


@bot.command(pass_context=True, aliases=['r', 'res'])
async def старт(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Старт")
        voice.resume()
        await ctx.send("Старт")
    else:
        print("Музыка не на паухе")
        await ctx.send("Музыка не на паузе")


@bot.command(pass_context=True, aliases=['s', 'sto'])
async def стоп(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Стоп")
        voice.stop()
        await ctx.send("Стоп")
    else:
        print("Не удалось остановить воспроизведение музыки")
        await ctx.send("Не удалось остановить воспроизведение музыки")


queues = {}

@bot.command(pass_context=True, aliases=['q', 'que'])
async def очередь(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Скачивание аудио\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)


    await ctx.send("Добавлена песня " + str(q_num) + " в очередь")

    print("Добавлена песня в очередь\n")


@bot.command(pass_context=True, aliases=['n', 'nex'])
async def скип(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Воспроизведение следующей песни")
        voice.stop()
        await ctx.send("Следущая песня")
    else:
        print("Музыка не играет")
        await ctx.send("Воспроизведение музыки приостановлено")


@bot.command()
async def отнимание(ctx, a: int, b: int):
    await ctx.send(a-b)

@bot.command()
async def деление(ctx, a: int, b: int):
    await ctx.send(a/b)

@bot.command()
async def степень(ctx, a: int, b: int):
    await ctx.send(a**b)

@bot.command()
async def сумма(ctx, a: int, b: int):
    await ctx.send(a+b)


@bot.command()
async def умножить(ctx, a: int, b: int):
    await ctx.send(a*b)


@bot.command()
async def ролл(ctx):
    num = random.randint(0, 100)
    await ctx.send(str(num)  + "{}".format(ctx.author.mention))


@bot.command(pass_context=True)
async def f(ctx, arg: discord.Member = None):
    if not arg:
        author = ctx.message.author
        emb = discord.Embed(title=f'{author.name} press F to pay respect', colour=0x333333)
        await ctx.send(embed=emb)
    else:
        author = ctx.message.author
        emb = discord.Embed(title=f'{author.name} press F to pay respect' + f' {arg.name}', colour=0x333333)
        await ctx.send(embed=emb)

@bot.command()
async def аватар(ctx, member : discord.Member = None):
    user = ctx.message.author if (member == None) else member
    await ctx.message.delete()
    embed = discord.Embed(title=f'Аватар пользователя {user}', description= f'[Ссылка на изображение]({user.avatar_url})', color=user.color)
    embed.set_footer(text= f'Вызвано: {ctx.message.author}', icon_url= str(ctx.message.author.avatar_url))
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def флип(ctx):
    num=random.randint(1,2)
    if (num == 1):
           await ctx.send("Вым выпал -Орёл")
           print("[?coin] - done")
    if(num == 2):
           await ctx.send("Вам выпала -Решка")
           print("[?coin] - done")

@bot.command()
async def привет(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет, куколд <@{author.id}>")

@bot.command()
async def Привет(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет, куколд <@{author.id}>")

@bot.command()
@commands.has_permissions(administrator = True) # Могут использовать лишь пользователи с правами Администратора
async def say(ctx, channel: discord.TextChannel, *, cnt):
   await ctx.message.delete() # Удаляет написанное вами сообщение
   embed = discord.Embed(description = cnt, colour = 0x00ff80) # Генерация красивого сообщения
   await channel.send(embed=embed) # Отправка сообщения в указанный Вами канал


token = os.environ.get('BOT_TOKEN')


bot.run(str(token))

