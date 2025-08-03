CREATE TABLE recordatorio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    asunto TEXT,
    fecha DATETIME,
    created_at DATETIME,
    status TEXT
);
