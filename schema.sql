CREATE TABLE
    recordatorio (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        usuario_id BIGINT,
        asunto TEXT,
        fecha DATETIME,
        created_at DATETIME,
        status VARCHAR(3)
    );