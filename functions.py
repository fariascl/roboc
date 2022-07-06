def get_apibay(term: str):
    from requests import get
    APIBAY = 'https://apibay.org/q.php?q='
    if (term):
        res = get(f'{APIBAY}{term}').json()
        rows = res
        #for row in row:
        #    title = row['title']
        #    size = row['size']
        #    seeders = row['seeders']
        #    leechers = row['leechers']
        #    hash = row['info_hash']
        return rows[0]
 
def tuple2string(tupla):
    streeng = ''
    for item in tupla:
        streeng = streeng + item + ' '
    return streeng


def get_clima(ciudad: str):
    import json, xmltodict
    from requests import get
    from constants import API_CLIMA, API_CLIMA_KEY
    if (ciudad):
        response = get(f'{API}{ciudad}')
        yeison = json.loads(response.content)
        id_ciudad = yeison['localidad'][0]['id']
        response_final = get(f'http://api.meteored.cl/index.php?api_lang=cl&localidad={id_ciudad}&affiliate_id={API_KEY}')
        xml_clima = xmltodict.parse(response_final.content)
        nombre_ciudad = xml_clima['report']['location']['@city']
        maxima_hoy = xml_clima['report']['location']['var'][1]['data']['forecast'][0]
        return nombre_ciudad, maxima_hoy

