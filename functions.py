import json
import requests
import meteoredpy
import os
from dotenv import load_dotenv

load_dotenv()


def get_apibay(term: str):
    APIBAY = 'https://apibay.org/q.php?q='
    if (term):
        rows = requests.get(f'{APIBAY}{term}').json()
        return rows[0]


def tuple2string(tupla):
    return ' '.join(tupla)


def get_clima(ciudad: str):
    # Convierte los parámetros en una cadena, por ejemplo: ['Viña','del','Mar'] a 'Viña del Mar'
    ciudad = tuple2string(ciudad)
    clima = meteoredpy(os.getenv('API_CLIMA_KEY')).get(ciudad)
    msg = f"La máxima de hoy para {clima['ciudad']} será de {clima['maxima']} °C"
    return msg


def get_pregunta():
    import random
    respuesta = random.randint(1, 3)

    if respuesta == 1:
        msg = "**Sí**"

    if respuesta == 2:
        msg = "**No**"

    if respuesta == 3:
        msg = "**Puede ser..**"
    return respuesta


def get_temblor():
    from datetime import datetime
    page = requests.get("https://api.gael.cloud/general/public/sismos")
    temblor = json.loads(page.content)  # JSON con el último temblor
    fecha = datetime.strptime(
        temblor['Fecha'], "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y a las %H:%M:%S")
    latitud, longitud, profundidad, magnitud, refgeo = temblor['Latitud'], temblor[
        'Longitud'], temblor['Profundidad'], temblor['Magnitud'], temblor['RefGeografica']
    msg = f"El último temblor fue el {fecha}, a {refgeo} y tuvo una magnitud de {magnitud}"
    return msg


# Hay que ver después

# (COMANDO 3 - PABLO) Funcion para asignar la opcion elegida version Texto.
def setOpcionCachipun(opcion):
    if opcion == 1:
        return "PIEDRA"

    if opcion == 2:
        return "PAPEL"

    if opcion == 3:
        return "TIJERA"


def get_cachipun(usuario1, usuario2):
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

    return msg


def get_torrent(term):
    try:
        term = tuple2string(term)
        row = get_apibay(term)
        msg = f"Título: `{row['name']}`\n:hash:: `{row['info_hash']}`\n:arrow_up:: `{row['seeders']}`\n:arrow_down:: `{row['leechers']}`\n"
        msg += f":magnet:: `magnet:?xt=urn:btih:{row['info_hash']}&dn={row['name']}&tr=udp://tracker.cubonegro.lol:6969/announce&tr=udp://open.tracker.cl:6969/announce`"
        return msg
    except Exception as e:
        msg = f"Ha ocurrido un error ({e}) al buscar, consulta más tarde"
        print(msg)
        return msg
