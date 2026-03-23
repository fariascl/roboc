CREATE TABLE IF NOT EXISTS recordatorio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    asunto TEXT,
    fecha DATETIME,
    created_at DATETIME,
    status TEXT
);

CREATE TABLE IF NOT EXISTS command_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    usuario_name TEXT,
    channel_id INTEGER,
    guild_id INTEGER,
    comando TEXT,
    parametros TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
