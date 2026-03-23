import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import os
import functions
import helpers
import classes.recordatorio as recordatorio
import yt_dlp
import re

# ======================================
# CONFIGURACIÓN DEL BOT
# ======================================
__version__ = "1.0.0"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", description="Bot para todo uso", intents=intents)
music_queues = {}

# ======================================
# COMANDOS BÁSICOS
# ======================================

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="ℹ️ Información del Bot", color=discord.Color.blue())
    embed.add_field(name="Versión", value=f"`{__version__}`", inline=False)
    embed.add_field(name="Latencia (Ping)", value=f"`{round(bot.latency * 1000)}ms`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ayuda(ctx):
    msg = "**Hola!, soy roboc, un 🤖 para todo uso**\n"
    msg += f"Versión: `{__version__}`\n"
    msg += "Los comandos disponibles son: \n"
    msg += '\n**`/recordar`** pone un recordatorio :alarm_clock:. Ej: `/recordar tarea 05-08-2025 21:30`'
    msg += "\n\n**`/clima`** muestra la temperatura máxima :partly_sunny: en una ciudad."
    msg += "\n\n**`/temblor`** muestra el último temblor registrado"
    msg += "\n\n**`/dado`** lanza un dado :game_die:"
    msg += "\n\n**`/pregunta`** responde preguntas al azar"
    msg += "\n\n**`/cachipun`** juega cachipún entre dos usuarios :fist: :v:"
    msg += "\n\n**`/acortar`** genera una URL corta :link:"
    msg += "\n\n**🎵 Comandos de música:** `/join`, `/play <nombre o link>`, `/skip`, `/stop`, `/disconnect`"
    await ctx.send(msg)

# ======================================
# COMANDOS VARIOS
# ======================================

@bot.command()
async def temblor(ctx):
    try:
        msg = functions.get_temblor()
    except Exception as e:
        helpers.log_to_file("/temblor", e, "ERROR")
        msg = f"Error al obtener /temblor: {e}"
    await ctx.send(msg)

@bot.command()
async def clima(ctx, *args):
    try:
        msg = functions.get_clima(args)
    except Exception as e:
        helpers.log_to_file("/clima", e, "ERROR")
        msg = f"Error al obtener /clima: {e}"
    await ctx.send(msg)

@bot.command()
async def dado(ctx):
    try:
        msg = functions.get_dado()
    except Exception as e:
        helpers.log_to_file("/dado", e, "ERROR")
        msg = f"Error al obtener /dado: {e}"
    await ctx.send(msg)

@bot.command()
async def pregunta(ctx):
    try:
        msg = functions.get_pregunta()
    except Exception as e:
        helpers.log_to_file("/pregunta", e, "ERROR")
        msg = f"Error al obtener /pregunta: {e}"
    await ctx.send(msg)

@bot.command()
async def cachipun(ctx, usuario1: discord.User, usuario2: discord.User):
    try:
        msg = functions.get_cachipun(usuario1, usuario2)
    except Exception as e:
        helpers.log_to_file("/cachipun", e, "ERROR")
        msg = f"Error al ejecutar /cachipun: {e}"
    await ctx.send(msg)

@bot.command()
async def acortar(ctx, *args):
    try:
        msg = functions.get_acortar(args)
    except Exception as e:
        helpers.log_to_file("/acortar", e, "ERROR")
        msg = f"Error al ejecutar /acortar: {e}"
    await ctx.send(msg)

# ======================================
# RECORDATORIOS
# ======================================

@bot.command()
async def recordar(ctx, *args):
    try:
        if len(args) < 3:
            await ctx.send("Uso: `/recordar tarea 05-08-2025 21:30`")
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
        await ctx.send(f"Error al ejecutar /recordar: {e}")

@bot.command()
async def recordatorios(ctx):
    try:
        msg = recordatorio.Recordatorio().get_recordatorios(ctx.author.id)[0]
    except Exception as e:
        helpers.log_to_file("/recordatorios", e, "ERROR")
        msg = f"Error al obtener /recordatorios: {e}"
    await ctx.send(msg)

@bot.command()
async def parar(ctx):
    try:
        msg = recordatorio.Recordatorio().stop_recordatorio(ctx.author.id)
    except Exception as e:
        helpers.log_to_file("/parar", e, "ERROR")
        msg = f"Error al ejecutar /parar: {e}"
    await ctx.send(msg)

# ======================================
# MÚSICA
# ======================================

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"✅ Me uní al canal de voz **{channel.name}**")
    else:
        await ctx.send("⚠️ Únete a un canal de voz primero")

def search_youtube(query):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'tv_embedded'],
            }
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            if re.match(r'https?://', query):
                return ydl.extract_info(query, download=False)
            else:
                info = ydl.extract_info(f"ytsearch5:{query}", download=False)
                for entry in info['entries']:
                    if 'url' in entry:
                        return entry
        except Exception as e:
            print(f"Error buscando: {e}")
            return None

@bot.command()
async def play(ctx, *, query: str):
    try:
        if not ctx.author.voice:
            return await ctx.send("⚠️ Únete a un canal de voz primero")

        voice_client = ctx.voice_client
        if not voice_client:
            voice_client = await ctx.author.voice.channel.connect()

        info = search_youtube(query)
        if not info:
            return await ctx.send("❌ No se pudo encontrar la canción")

        source_url = info['url']
        title = info.get('title', 'Desconocido')

        guild_id = ctx.guild.id
        if guild_id not in music_queues:
            music_queues[guild_id] = []
        music_queues[guild_id].append((source_url, title))

        await ctx.send(f"🎶 **{title}** agregada a la cola")

        if not voice_client.is_playing():
            await play_next(ctx)
    except Exception as e:
        helpers.log_to_file("/play", str(e), "ERROR")
        await ctx.send(f"⚠️ Error al reproducir: {e}")

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

    ffmpeg_opts = "-vn -loglevel error -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -re"
    try:
        audio_source = discord.FFmpegPCMAudio(source_url, before_options=ffmpeg_opts, options="-vn")
        ctx.voice_client.play(audio_source, after=after_playing)
        await ctx.send(f"▶️ Reproduciendo: **{title}**")
    except Exception as e:
        print(f"Error al reproducir: {e}")
        await ctx.send("⚠️ No se pudo reproducir esa canción, intentando la siguiente...")
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
        await ctx.send("⏹ Música detenida y cola limpiada")
    else:
        await ctx.send("⚠️ No hay música en reproducción")

@bot.command()
async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        music_queues[ctx.guild.id] = []
        await ctx.send("👋 Me desconecté del canal de voz")
    else:
        await ctx.send("⚠️ No estoy en ningún canal de voz")

# ======================================
# EVENTOS
# ======================================

@tasks.loop(minutes=1.0)
async def check_recordatorios():
    try:
        recordatorios_pendientes = recordatorio.Recordatorio().execute_recordatorios()
        if recordatorios_pendientes and recordatorios_pendientes != -1:
            for rec in recordatorios_pendientes:
                rec_id = rec[0]
                user_id = rec[1]
                asunto = rec[2]
                
                user = await bot.fetch_user(user_id)
                if user:
                    try:
                        await user.send(f"⏰ **¡RECORDATORIO!** ⏰\n\nHola, me pediste que te recordara lo siguiente:\n> {asunto}")
                    except discord.Forbidden:
                        print(f"No pude enviar DM a {user.name}")
                
                recordatorio.Recordatorio().mark_as_done(rec_id)
    except Exception as e:
        helpers.log_to_file("check_recordatorios", e, "ERROR")

@check_recordatorios.before_loop
async def before_check_recordatorios():
    await bot.wait_until_ready()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/ayuda"))
    check_recordatorios.start()
    print(f"🤖 El bot está listo como {bot.user}")

@bot.event
async def on_command(ctx):
    comando = ctx.command.name if ctx.command else "unknown"
    parametros = str(ctx.args) if ctx.args else ""
    if ctx.kwargs:
        parametros += f" {ctx.kwargs}"
    helpers.log_command(ctx, comando, parametros)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(":see_no_evil: Comando no encontrado")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":exclamation: Faltan argumentos")
    else:
        helpers.log_to_file("on_command_error", str(error), "ERROR")
        await ctx.send(f"Ocurrió un error: {error}")

# ======================================
# EJECUCIÓN
# ======================================
bot.run(os.getenv("TOKEN"))
