import discord
from discord.ext import commands
import asyncio
import datetime
import os
import functions
import helpers
import classes.recordatorio as recordatorio
import yt_dlp

# Crear bot
bot = commands.Bot(command_prefix="/", description="Bot para todo uso", intents=discord.Intents.all())

# Diccionario de colas por servidor
music_queues = {}

# ==================== COMANDOS EXISTENTES ====================

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def ayuda(ctx):
    msg = "**Hola!, soy roboc, un :robot: para todo uso**\n"
    msg += "Los comandos disponibles son: \n"
    msg += '\n**`/recordar`** permite poner un recordatorio :alarm_clock:.\n> **Uso:** /recordar "asunto" dd-MM-AA hh:mm'
    msg += "\n\n**`/clima`** permite ver la temperatura :partly_sunny: máxima en alguna ciudad."
    msg += "\n\n**`/temblor`** permite ver el último temblor registrado"
    msg += "\n\n**`/dado`** permite lanzar un dado :game_die:"
    msg += "\n\n**`/pregunta`** permite preguntar"
    msg += "\n\n**`/cachipun`** permite jugar al cachipún :fist: :v:"
    msg += "\n\n**`/acortar`** permite generar una URL corta"
    msg += "\n\n**`/ayuda`** permite ver este mensaje\n"
    await ctx.send(msg)

@bot.command()
async def temblor(ctx):
    try:
        msg = functions.get_temblor()
    except Exception as e:
        helpers.log_to_file("/temblor", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/temblor`"
    await ctx.send(msg)

@bot.command()
async def clima(ctx, *args):
    try:
        msg = functions.get_clima(args)
    except Exception as e:
        helpers.log_to_file("/clima", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/clima`"
    await ctx.send(msg)

@bot.command()
async def dado(ctx):
    try:
        msg = functions.get_dado()
    except Exception as e:
        helpers.log_to_file("/dado", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/dado`"
    await ctx.send(msg)

@bot.command()
async def pregunta(ctx):
    try:
        msg = functions.get_pregunta()
    except Exception as e:
        helpers.log_to_file("/pregunta", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/pregunta`"
    await ctx.send(msg)

@bot.command()
async def cachipun(ctx, usuario1: discord.User, usuario2: discord.User):
    try:
        msg = functions.get_cachipun(usuario1, usuario2)
    except Exception as e:
        helpers.log_to_file("/cachipun", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al ejecutar `/cachipun`"
    await ctx.send(msg)

@bot.command()
async def acortar(ctx, *args):
    try:
        msg = functions.get_acortar(args)
    except Exception as e:
        helpers.log_to_file("/acortar", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al ejecutar `/acortar`"
    await ctx.send(msg)

# ==================== COMANDOS DE RECORDATORIOS ====================

@bot.command()
async def recordar(ctx, *args):
    try:
        if len(args) < 3:
            await ctx.send("Proporciona asunto, fecha y hora. Ej: `/recordar tarea 05-08-2025 21:30`")
            return
        fecha_input = args[-2].lower()
        hora_input = args[-1]

        if fecha_input == "hoy":
            today_str = datetime.datetime.now().strftime("%d-%m-%Y")
            fecha_hora_received = f"{today_str} {hora_input}"
        else:
            fecha_hora_received = f"{fecha_input} {hora_input}"

        fecha_hora_parsed = datetime.datetime.strptime(fecha_hora_received, "%d-%m-%Y %H:%M")
        fecha_hora = fecha_hora_parsed.strftime("%Y-%m-%d %H:%M")

        asunto = helpers.tuple2string(args[0 : len(args) - 2])
        msg = recordatorio.Recordatorio().create_recordatorio(ctx.author.id, asunto, fecha_hora)
        await ctx.send(msg)
    except Exception as e:
        helpers.log_to_file("/recordar", e, "ERROR")
        await ctx.send(f"Ha ocurrido un problema ({e}) al ejecutar `/recordar`")

@bot.command()
async def recordatorios(ctx):
    try:
        msg = recordatorio.Recordatorio().get_recordatorios(ctx.author.id)[0]
    except Exception as e:
        helpers.log_to_file("/recordatorios", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/recordatorios`"
    await ctx.send(msg)

@bot.command()
async def parar(ctx):
    try:
        msg = recordatorio.Recordatorio().stop_recordatorio(ctx.author.id)
    except Exception as e:
        helpers.log_to_file("/parar", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al ejecutar `/parar`"
    await ctx.send(msg)

# ==================== COMANDOS DE MUSICA ====================

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"✅ Me uní al canal de voz {channel.name}")
    else:
        await ctx.send("⚠️ Únete a un canal de voz primero")

@bot.command()
async def play(ctx, *, url_or_search: str):
    voice_client = ctx.voice_client
    if not voice_client:
        if ctx.author.voice:
            voice_client = await ctx.author.voice.channel.connect()
        else:
            return await ctx.send("⚠️ Únete a un canal de voz primero")

    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url_or_search, download=False)
        except Exception as e:
            return await ctx.send(f"❌ No pude encontrar la canción: {e}")

    source_url = info['url']
    title = info.get('title', 'Desconocido')

    guild_id = ctx.guild.id
    if guild_id not in music_queues:
        music_queues[guild_id] = []
    music_queues[guild_id].append((source_url, title))

    await ctx.send(f"🎵 **{title}** agregada a la cola")

    if not voice_client.is_playing():
        await play_next(ctx)

async def play_next(ctx):
    guild_id = ctx.guild.id
    if not music_queues.get(guild_id):
        await ctx.voice_client.disconnect()
        return

    source_url, title = music_queues[guild_id].pop(0)

    def after_playing(error):
        fut = asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(f"Error after_playing: {e}")

    ctx.voice_client.play(discord.FFmpegPCMAudio(source_url, options='-vn'), after=after_playing)
    await ctx.send(f"▶️ Reproduciendo: **{title}**")

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭ Canción saltada")
    else:
        await ctx.send("⚠️ No hay canción reproduciéndose")

@bot.command()
async def stop(ctx):
    guild_id = ctx.guild.id
    if ctx.voice_client:
        ctx.voice_client.stop()
        music_queues[guild_id] = []
        await ctx.send("⏹ Música detenida y cola eliminada")
    else:
        await ctx.send("⚠️ No estoy reproduciendo nada")

@bot.command()
async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        music_queues[ctx.guild.id] = []
        await ctx.send("✅ Me desconecté del canal de voz")
    else:
        await ctx.send("⚠️ No estoy en ningún canal de voz")

# ==================== EVENTOS ====================

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/ayuda"))
    print("El 🤖 está listo")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(":see_no_evil: Comando no encontrado")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":exclamation: Faltan argumentos")
    elif isinstance(error, commands.UserNotFound):
        await ctx.send(":people_wrestling: Usuario no encontrado")
    else:
        await ctx.send(f"Ocurrió un error: {error}")

# ==================== RUN ====================
bot.run(os.getenv("TOKEN"))
