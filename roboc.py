import discord
from discord.ext import commands
import asyncio
import datetime
import os
import functions
import helpers
import classes.recordatorio as recordatorio
import yt_dlp
import re
import requests

# ----------------- CONFIG -----------------
bot = commands.Bot(
    command_prefix="/",
    description="Bot para todo uso",
    intents=discord.Intents.all()
)

music_queues = {}  # Diccionario de colas por servidor

FFMPEG_OPTIONS = {
    'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

# ----------------- COMANDOS GENERALES -----------------
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def ayuda(ctx):
    msg = "**Hola!, soy roboc, un :robot: para todo uso**\n"
    msg += "Los comandos disponibles son: \n"
    msg += '\n**`/recordar`** permite poner un recordatorio :alarm_clock:.\n> Uso: /recordar "asunto" dd-MM-AA hh:mm'
    msg += "\n**`/clima`** permite ver la temperatura"
    msg += "\n**`/temblor`** permite ver el último temblor registrado"
    msg += "\n**`/dado`** permite lanzar un dado"
    msg += "\n**`/pregunta`** permite preguntar"
    msg += "\n**`/cachipun`** permite jugar al cachipún"
    msg += "\n**`/acortar`** permite generar una URL corta"
    msg += "\n**`/ayuda`** muestra este mensaje"
    await ctx.send(msg)

# ----------------- COMANDOS DE RECORDATORIOS -----------------
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

# ----------------- COMANDOS DE MUSICA -----------------
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"✅ Me uní al canal de voz {channel.name}")
    else:
        await ctx.send("⚠️ Únete a un canal de voz primero")

def get_audio_source_embed(query: str):
    """Devuelve URL, título, miniatura y duración para embed."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'default_search': 'auto'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            info = info['entries'][0]

    url = info['url']
    title = info.get('title', 'Desconocido')
    thumbnail = info.get('thumbnail', None)
    duration = str(datetime.timedelta(seconds=info.get('duration', 0)))
    return url, title, thumbnail, duration

async def play_next(ctx):
    """Reproduce la siguiente canción en la cola con embed."""
    guild_id = ctx.guild.id
    if not music_queues.get(guild_id):
        await asyncio.sleep(2)
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        await ctx.send("📭 Cola vacía, desconectándome.")
        return

    source_url, title, thumbnail, duration = music_queues[guild_id].pop(0)
    voice_client = ctx.voice_client

    def after_playing(error):
        if error:
            print(f"Error al reproducir: {error}")
        fut = asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(f"Error en after_playing: {e}")

    try:
        source = discord.FFmpegPCMAudio(source_url, **FFMPEG_OPTIONS)
        voice_client.play(source, after=after_playing)

        embed = discord.Embed(
            title="▶️ Reproduciendo ahora",
            description=f"[{title}](https://www.youtube.com/results?search_query={title.replace(' ', '+')})",
            color=discord.Color.green()
        )
        embed.add_field(name="Duración", value=duration, inline=True)
        embed.add_field(name="Solicitado por", value=ctx.author.mention, inline=True)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Error al reproducir: `{e}`")
        print(f"[FFmpeg error] {e}")
        await play_next(ctx)

@bot.command()
async def play(ctx, *, query: str):
    voice_client = ctx.voice_client
    if not voice_client:
        if ctx.author.voice:
            voice_client = await ctx.author.voice.channel.connect()
        else:
            return await ctx.send("⚠️ Únete a un canal de voz primero.")

    # Si es un enlace de Spotify → obtenemos título y artista
    if "spotify.com/track" in query:
        try:
            track_id = re.search(r"track/([A-Za-z0-9]+)", query).group(1)
            r = requests.get(f"https://open.spotify.com/oembed?url=https://open.spotify.com/track/{track_id}")
            data = r.json()
            query = data["title"]
            await ctx.send(f"🎧 Buscando en YouTube: `{query}`")
        except Exception as e:
            return await ctx.send(f"❌ No pude leer la canción de Spotify: `{e}`")

    try:
        source_url, title, thumbnail, duration = get_audio_source_embed(query)
    except Exception as e:
        return await ctx.send(f"❌ Error al obtener el audio: `{e}`")

    guild_id = ctx.guild.id
    if guild_id not in music_queues:
        music_queues[guild_id] = []
    music_queues[guild_id].append((source_url, title, thumbnail, duration))

    await ctx.send(f"🎵 **{title}** agregada a la cola")

    if not voice_client.is_playing():
        await play_next(ctx)

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

# ----------------- EVENTOS -----------------
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

# ----------------- RUN -----------------
bot.run(os.getenv("TOKEN"))
