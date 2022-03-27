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
