# helpers.py
import os
from datetime import datetime

def is_empty_or_whitespace(s):
    return not s or s.strip() == ''

def tuple2string(tupla):
    return ' '.join(tupla)

def log_to_file(function, message, prefix=''):
    """
    Params:
    - function (str): El nombre de la función donde ocurrió.
    - message (str): El mensaje a registrar.
    - prefix (str): Un prefijo opcional para el nombre del archivo.
    """
    # Directorio base del proyecto (afuera de src/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    storage_path = os.getenv('LOG_PATH', os.path.join(base_dir, 'storage', 'logs'))
    
    # Crear carpeta de logs si no existe
    os.makedirs(storage_path, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_filename = f"{prefix}-{date_str}.log" if prefix else f"{date_str}.log"
    full_path = os.path.join(storage_path, log_filename)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{prefix}] {function}: {message}\n"
    
    with open(full_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)
        
    # Imprimir a consola para que Docker (o la terminal) pueda verlo
    print(log_entry.strip())
