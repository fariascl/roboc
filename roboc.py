import discord
from discord.ext import commands
from constants import TOKEN
bot = commands.Bot(command_prefix="/", description="este es un bot de prueba")


def getTemblor():
    import requests, json
    page = requests.get("https://api.gael.cloud/general/public/sismos")
    yeison = json.loads(page.content)
    return yeison[0]

# (COMANDO 3 - PABLO) Funcion para asignar la opcion elegida version Texto.
def setOpcionCachipun(opcion):
    if opcion == 1:
        return "PIEDRA"
    
    if opcion == 2:
        return "PAPEL"

    if opcion == 3:
        return "TIJERA"

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

@bot.command()
async def buscar(ctx, *args):
    from functions import get_apibay, tuple2string
    print(args)
    term = tuple2string(args)
    row = get_apibay(term)
    msg = f"Título: `{row['name']}`\nHash: `{row['info_hash']}`\nSE: `{row['seeders']}`\nLE: `{row['leechers']}`\n"
    msg += f"Enlace magnético: `magnet:?xt=urn:btih:{row['info_hash']}&dn={row['name']}&tr=udp://tracker.dump.cl:6969/announce&tr=udp://open.tracker.cl:6969/announce`" 
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
async def pregunta(ctx, texto : str):
    import random
    respuesta = random.randint(1, 3)

    if respuesta == 1:
        msg = "**Sí**"

    if respuesta == 2:
        msg = "**No**"

    if respuesta == 3:
        msg = "**Puede ser..**"

    await ctx.send(msg)

# Comando 3 Cachipun - Pablo
@bot.command()
async def cachipun(ctx, usuario1: discord.User, usuario2: discord.User):
    import random

    eleccionUsuario1 = random.randint(1, 3)
    eleccionUsuario2 = random.randint(1, 3)

    opcion1 = setOpcionCachipun(eleccionUsuario1)
    opcion2 = setOpcionCachipun(eleccionUsuario2)

    '''
        1) Piedra
        2) Papel
        3) Tijera
    '''
    # Empate
    if eleccionUsuario1 == eleccionUsuario2:
        msg = f"**{opcion1}** vs **{opcion2}** || **EMPATE!!**"

    if eleccionUsuario1 == 1 and eleccionUsuario2 == 2:
        msg = f"**{opcion1}** vs **{opcion2}** || **GANA {usuario2}**"

    if eleccionUsuario1 == 1 and eleccionUsuario2 == 3:
        msg = f"**{opcion1}** vs **{opcion2}** || **GANA {usuario1}**"

    if eleccionUsuario1 == 2 and eleccionUsuario2 == 1:
        msg = f"**{opcion1}** vs **{opcion2}** || **GANA {usuario1}**"

    if eleccionUsuario1 == 2 and eleccionUsuario2 == 3:
        msg = f"**{opcion1}** vs **{opcion2}** || **GANA {usuario2}**"

    if eleccionUsuario1 == 3 and eleccionUsuario2 == 1:
        msg = f"**{opcion1}** vs **{opcion2}** || **GANA {usuario2}**"

    if eleccionUsuario1 == 3 and eleccionUsuario2 == 2:
        msg = f"**{opcion1}** vs **{opcion2}** || **GANA {usuario1}**"

    await ctx.send(msg)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/help'))
    print("El bot está listo")
bot.run(TOKEN)
