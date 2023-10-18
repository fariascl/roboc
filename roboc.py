import discord
from discord.ext import commands
from functions import *
import asyncio
import datetime
import classes.recordatorio as recordatorio
bot = commands.Bot(command_prefix="/", description="Bot para hacer cosas")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def ayuda(ctx):
    msg = "Hola!, soy roboc, un :robot: para todo uso\n"
    msg += "Los comandos disponibles son: \n"
    msg += "`/recordar` permite poner un recordatorio :alarm_clock:. Uso: `/recordar \"asunto\" dd-MM-AA hh:mm` \n"
    msg += "`/clima` permite ver la temperatura :partly_sunny: máxima en alguna ciudad. Uso: `/clima conce`\n"
    msg += "`/temblor` permite ver el último temblor registrado\n"
    msg += "`/torrent` permite buscar torrents relacionados a un título. Uso: `/torrent los simpson`\n"
    msg += "`/dado` permite lanzar un dado :game_dice: \n"
    msg += "`/pregunta` permite preguntar. Uso: `/pregunta \"me irá bien en el certamen?\"`\n"
    msg += "`/cachipun` permite jugar al cachipún :fist:  :leftwards_hand: (al azar) entre dos usuarios. Uso `/cachipun @usuarioA @usuarioB`\n"
    msg += "`/ayuda` permite ver este mensaje\n"
    await ctx.send(msg)

@bot.command()
async def temblor(ctx):
    try:
        msg = get_temblor()
        await ctx.send(msg)
    except:
        msg = "Ha ocurrido un problema al obtener el último temblor, consulta más tarde"
        await ctx.send(msg)


@bot.command()
async def torrent(ctx, *args):
    torrent = get_torrent(args)
    await ctx.send(torrent)


@bot.command()
async def clima(ctx, *args):
    try:
        from functions import get_clima, tuple2string
        msg = get_clima(args)
        await ctx.send(msg)
    except:
        msg = "Ha ocurrido un problema al obtener el clima, consulta más tarde"
        await ctx.send(msg)


# Comando prueba Pablo
@bot.command()
async def dado(ctx):
    import random
    numero = random.randint(1, 6)
    msg = f":game_die: **Dado lanzado** :game_die: {numero}"
    await ctx.send(msg)

# Comando 2 prueba Pablo


@bot.command()
async def pregunta(ctx):
    msg = get_pregunta()
    await ctx.send(msg)

# Comando 3 Cachipun - Pablo


@bot.command()
async def cachipun(ctx, usuario1: discord.User, usuario2: discord.User):
    msg = get_cachipun(usuario1, usuario2)
    await ctx.send(msg)


@bot.command()
async def recordar(ctx: commands.context.Context, *args):
    try:
        asunto = tuple2string(args[0:len(args)-2])
        print(asunto)
        fecha_hora_received = f"{args[len(args)-2]} {args[len(args)-1]}"
        fecha_hora_parsed = datetime.datetime.strptime(
            fecha_hora_received, "%d-%m-%Y %H:%M")
        dia = fecha_hora_parsed.day
        mes = fecha_hora_parsed.month
        anio = fecha_hora_parsed.year
        hora = fecha_hora_parsed.hour
        minutos = fecha_hora_parsed.minute
        fecha_hora = f"{anio}-{mes}-{dia} {hora}:{minutos}"
        # usuario_id, asunto, fecha
        msg = recordatorio.Recordatorio().create_recordatorio(
            ctx.author.id, asunto, fecha_hora)
        await ctx.send(msg)
    except Exception as e:
        print(e)


@bot.command()
async def recordatorios(ctx: commands.context.Context):
    msg = recordatorio.Recordatorio().get_recordatorios(ctx.author.id)[0]
    await ctx.send(msg)


@bot.command()
async def parar(ctx: commands.context.Context):
    msg = recordatorio.Recordatorio().stop_recordatorio(ctx.author.id)
    await ctx.send(msg)


async def recordando(recordatorios):
    try:
        if (len(recordatorios) > 0):
            for recordatorio in recordatorios:
                usuario = await bot.fetch_user(recordatorio[0])
                if usuario and recordatorio[4] == 'on':
                    # usuario_id, asunto, fecha, created_at
                    await usuario.send(f"¡Riiing, riiing! RECORDATORIO: {recordatorio[1]}, Fecha:{recordatorio[2]}")
    except Exception as e:
        #print(e)
        print("Error al recordar")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/ayuda'))
    print("El bot está listo")
    while True:
        recordatorios = recordatorio.Recordatorio().execute_recordatorios()
        if recordatorios != -1:
            #print("Ejecutando recordatorios")
            await recordando(recordatorios)  # Llama a tu función
        #else:
            #print("No hay recordatorios")
        await asyncio.sleep(3)

bot.run(os.getenv('TOKEN'))
