# helpers.py

def is_empty_or_whitespace(s):
    return not s or s.strip() == ''

def tuple2string(tupla):
    return ' '.join(tupla)


# helpers.py

from datetime import datetime

def log_to_file(function ,message, prefix=''):
    storage_path = './storage/logs'
    """    
    Params:
    - message (str): El mensaje a registrar.
    - prefix (str): Un prefijo opcional para el nombre del archivo.
    """
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_filename = f"{prefix}-{date_str}.log"
    full_path = f"{storage_path}/{log_filename}"

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(full_path, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {function}: {message}\n")

