import discord
from discord.ext import commands
from constants import TOKEN
bot = commands.Bot(command_prefix="/", description="este es un bot de prueba")


def getTemblor():
    import requests, json
    page = requests.get("https://api.gael.cloud/general/public/sismos")
    yeison = json.loads(page.content)
    return yeison[0]


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def temblor(ctx):
    from datetime import datetime
    temblor = getTemblor()
    fecha_api = temblor['Fecha']
    d = fecha_api
    fecha_aux = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    fecha = fecha_aux.strftime("%d-%m-%Y a las %H:%M:%S")
    print(fecha)
    latitud = temblor['Latitud']
    longitud = temblor['Longitud']
    profundidad = temblor['Profundidad']
    magnitud = temblor['Magnitud']
    refgeo = temblor['RefGeografica']
    msg = f"El último temblor fue el {fecha}, a {refgeo} y tuvo una magnitud de {magnitud}"
    await ctx.send(msg)

# Comando prueba Pablo
@bot.command()
async def dado(ctx):
    import random
    numero = random.randint(1, 6)
    msg = f"**Dado lanzado** -> {numero}"
    await ctx.send(msg)

# Comando 2 prueba Pablo
@bot.command()
async def pregunta(ctx, texto : str):
    import random
    respuesta = random.randint(1, 3)

    if respuesta == 1:
        msg = "Sí"

    if respuesta == 2:
        msg = "No"

    if respuesta == 3:
        msg = "Puede ser.."

    await ctx.send(msg)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/help'))
    print("El bot está listo")
bot.run(TOKEN)
