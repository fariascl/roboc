import discord
from discord.ext import commands
import functions
import asyncio
import datetime
import helpers
import classes.recordatorio as recordatorio
import os

bot = commands.Bot(command_prefix="/", description="Bot para hacer cosas")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def ayuda(ctx):
    msg = "**Hola!, soy roboc, un :robot: para todo uso**\n"
    msg += "Los comandos disponibles son: \n"
    msg += '\n**`/recordar`** permite poner un recordatorio :alarm_clock:.\n> **Uso:** __/recordar__ *"asunto" dd-MM-AA hh:mm*'
    msg += "\n\n**`/clima`** permite ver la temperatura :partly_sunny: máxima en alguna ciudad.\n> **Uso:** __/clima__ *conce*"
    msg += "\n\n**`/temblor`** permite ver el último temblor registrado"
    msg += "\n\n**`/dado`** permite lanzar un dado :game_die:"
    msg += '\n\n**`/pregunta`** permite preguntar.\n> **Uso:** __/pregunta__ *"me irá bien en el certamen?"*'
    msg += "\n\n**`/cachipun`** permite jugar al cachipún :fist: :leftwards_hand: :v: (al azar) entre dos usuarios.\n> **Uso:** __/cachipun__ *@usuarioA @usuarioB*"
    msg += "\n\n**`/acortar <link>`** permite generar una URL corta :link:.\n> **Uso:** __/acortar__ *https://ejemplo.com*"

    msg += "\n\n**`/ayuda`** permite ver este mensaje\n"
    await ctx.send(msg)


@bot.command()
async def temblor(ctx):
    try:
        msg = functions.get_temblor()
    except Exception as e:
        helpers.log_to_file("/temblor", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/temblor`, consulta más tarde"
    await ctx.send(msg)


@bot.command()
async def clima(ctx, *args):
    try:
        msg = functions.get_clima(args)
    except Exception as e:
        helpers.log_to_file("/clima", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/clima`, consulta más tarde"
    await ctx.send(msg)


# Comando prueba Pablo
@bot.command()
async def dado(ctx):
    try:
        msg = functions.get_dado()
    except Exception as e:
        helpers.log_to_file("/dado", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/dado`, consulta más tarde"
    await ctx.send(msg)


# Comando 2 prueba Pablo


@bot.command()
async def pregunta(ctx):
    try:
        msg = functions.get_pregunta()
    except Exception as e:
        helpers.log_to_file("/pregunta", e, "ERROR")
        msg = (
            f"Ha ocurrido un problema ({e}) al obtener `/pregunta`, consulta más tarde"
        )
    await ctx.send(msg)


# Comando 3 Cachipun - Pablo
@bot.command()
async def cachipun(ctx, usuario1: discord.User, usuario2: discord.User):
    try:
        msg = functions.get_cachipun(usuario1, usuario2)
    except Exception as e:
        print(type)
        helpers.log_to_file("/cachipun", e, "ERROR")
        msg = (
            f"Ha ocurrido un problema ({e}) al obtener `/cachipun`, consulta más tarde"
        )
    await ctx.send(msg)


@bot.command()
async def acortar(ctx: commands.context.Context, *args):
    try:
        msg = functions.get_acortar(args)
    except Exception as e:
        helpers.log_to_file("/acortar", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/acortar`, consulta más tarde"
    await ctx.send(msg)


@bot.command()
async def recordar(ctx: commands.context.Context, *args):
    try:
        if len(args) < 3:
            await ctx.send(
                "Por favor proporciona un asunto, fecha y hora :alarm_clock:. Ej: `/recordar tarea 05-08-2025 21:30`"
            )
            return

        # Detectar "hoy" como fecha
        fecha_input = args[-2].lower()
        hora_input = args[-1]

        if fecha_input == "hoy":
            today_str = datetime.datetime.now().strftime("%d-%m-%Y")
            fecha_hora_received = f"{today_str} {hora_input}"
        else:
            fecha_hora_received = f"{fecha_input} {hora_input}"

        # Parsear fecha y hora
        fecha_hora_parsed = datetime.datetime.strptime(
            fecha_hora_received, "%d-%m-%Y %H:%M"
        )
        fecha_hora = fecha_hora_parsed.strftime("%Y-%m-%d %H:%M")

        # Obtener asunto
        asunto = helpers.tuple2string(args[0 : len(args) - 2])

        # Guardar en base de datos
        msg = recordatorio.Recordatorio().create_recordatorio(
            ctx.author.id, asunto, fecha_hora
        )
        await ctx.send(msg)

    except Exception as e:
        helpers.log_to_file("/recordar", e, "ERROR")
        msg = (
            f"Ha ocurrido un problema ({e}) al ejecutar `/recordar`, intenta más tarde."
        )
        await ctx.send(msg)


@bot.command()
async def recordatorios(ctx: commands.context.Context):
    try:
        msg = recordatorio.Recordatorio().get_recordatorios(ctx.author.id)[0]
    except Exception as e:
        helpers.log_to_file("/recordar", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/recordatorios`, consulta más tarde"
    await ctx.send(msg)


@bot.command()
async def parar(ctx: commands.context.Context):
    try:
        msg = recordatorio.Recordatorio().stop_recordatorio(ctx.author.id)
    except Exception as e:
        helpers.log_to_file("/recordar", e, "ERROR")
        msg = f"Ha ocurrido un problema ({e}) al obtener `/parar`, consulta más tarde"
    await ctx.send(msg)


async def recordando(recordatorios):
    try:
        if len(recordatorios) > 0:
            for recordatorio in recordatorios:
                usuario = await bot.fetch_user(recordatorio[0])
                if usuario and recordatorio[4] == "on":
                    # usuario_id, asunto, fecha, created_at
                    await usuario.send(
                        f":alarm_clock:**¡Riiing, riiing!**:alarm_clock:\n:notepad_spiral:**RECORDATORIO:** {recordatorio[1]}\n:calendar:**Fecha:** {recordatorio[2]}"
                    )
    except Exception as e:
        helpers.log_to_file("recordando", e, "ERROR")
        print("Error al recordar")


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="/ayuda")
    )
    print("El 🤖 está listo")
    while True:
        recordatorios = recordatorio.Recordatorio().execute_recordatorios()
        if recordatorios != -1:
            # print("Ejecutando recordatorios")
            await recordando(recordatorios)  # Llama a tu función
        # else:
        # print("No hay recordatorios")
        await asyncio.sleep(3)
        
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(":see_no_evil: Comando no encontrado")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":exclamation: Faltan argumentos")
    elif isinstance(error, commands.UserNotFound):
        await ctx.send(":people_wrestling: Uno de los usuarios no existe, por favor etiqueta correctamente al usuario ")
    else:
        await ctx.send(f"Ocurrió un error: {error}")


bot.run(os.getenv("TOKEN"))
