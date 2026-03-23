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

def log_command(ctx, comando, parametros):
    """
    Registra un comando ejecutado por un usuario en la base de datos.
    Params:
    - ctx: El contexto del comando de Discord
    - comando (str): El nombre del comando ejecutado
    - parametros (str): Los parámetros pasados al comando
    """
    import sqlite3
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        db_path = os.getenv('DB_PATH', 'roboc.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        usuario_id = ctx.author.id
        usuario_name = str(ctx.author)
        channel_id = ctx.channel.id if hasattr(ctx, 'channel') and ctx.channel else None
        guild_id = ctx.guild.id if hasattr(ctx, 'guild') and ctx.guild else None
        
        query = """
        INSERT INTO command_log (usuario_id, usuario_name, channel_id, guild_id, comando, parametros)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (usuario_id, usuario_name, channel_id, guild_id, comando, parametros))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        log_to_file("log_command", str(e), "ERROR")
