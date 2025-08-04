import os
import json
import random
import requests
import helpers
from meteoredpy import Meteoredpy
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


def get_clima(ciudad: str):
    # Convierte los parámetros en una cadena, por ejemplo: ['Viña','del','Mar'] a 'Viña del Mar'
    ciudad = helpers.tuple2string(ciudad)
    if helpers.is_empty_or_whitespace(ciudad):
        msg = "El comando debe ser: `/clima conce`"
        return msg

    clima = Meteoredpy(os.getenv("API_CLIMA_TOKEN")).get(ciudad)
    msg = f"La máxima de hoy para {clima['ciudad']} será de {clima['maxima']} °C"
    return msg


def get_pregunta():
    respuestas = ["Sí", "No", "Puede ser.."]
    respuesta = random.randint(0, 2)
    msg = respuestas[respuesta]
    return f"**{msg}**"


def get_temblor():
    page = requests.get("https://api.cactuslab.cl/api/sismos/getLatest")
    temblor = json.loads(page.content)  # JSON con el último temblor

    temblor = temblor["sismos"][0]
    fecha = datetime.strptime(temblor["fecha"], "%Y-%m-%d %H:%M:%S").strftime(
        "%d-%m-%Y a las %H:%M:%S"
    )
    profundidad, magnitud, refgeo = (
        temblor["profundidad"],
        temblor["magnitud"],
        temblor["refgeo"],
    )
    msg = (
        f":earth_americas::boom: ¡Tembló!\n"
        f"El último sismo fue el {fecha}, cerca de {refgeo} :round_pushpin:\n"
        f":straight_ruler: Magnitud: {magnitud} :scales:\n"
        f":bell: ¡Recuerda tener listo tu kit de emergencia! :school_satchel::candle::radio:"
    )
    return msg


# Hay que ver después


# (COMANDO 3 - PABLO) Funcion para asignar la opcion elegida version Texto.
def setOpcionCachipun(opcion):
    opciones = [":rock:PIEDRA", ":roll_of_paper:PAPEL", ":scissors:TIJERA"]
    return opciones[opcion]


def get_cachipun(usuario1, usuario2):
    if (helpers.is_empty_or_whitespace(usuario1) or helpers.is_empty_or_whitespace(usuario2)):
        msg = "El comando debe ser: `/cachipun @usuario1 @usuario2`"
    eleccionUsuario1 = random.randint(0, 2)
    eleccionUsuario2 = random.randint(0, 2)

    opcion1 = setOpcionCachipun(eleccionUsuario1)
    opcion2 = setOpcionCachipun(eleccionUsuario2)

    # 0) Piedra
    # 1) Papel
    # 2) Tijera

    if eleccionUsuario1 == eleccionUsuario2:
        msg = f"**{opcion1}** vs **{opcion2}** || **EMPATE!!**"
    elif (eleccionUsuario1 - eleccionUsuario2) % 3 == 1:
        msg = f"**{opcion1}** vs **{opcion2}** || **GANA {usuario1}**"
    else:
        msg = f"**{opcion1}** vs **{opcion2}** || **GANA {usuario2}**"

    return msg


def get_dado():
    numero = random.randint(1, 6)
    msg = f":game_die: **Dado lanzado** :game_die:\n>             {numero}"
    return msg