-- ==========================================
-- City Routes: структура базы данных (SQLite)
-- ==========================================
--
-- interests 1:N users            (основной интерес пользователя)
-- interests 1:N routes           (тематика маршрута)
-- routes    1:N recommendations
-- users     1:N recommendations
--
-- IF NOT EXISTS позволяет выполнять скрипт повторно без ошибок.

CREATE TABLE IF NOT EXISTS interests (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    interest_id INTEGER NOT NULL,
    FOREIGN KEY (interest_id) REFERENCES interests(id)
);

CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    interest_id INTEGER NOT NULL,
    length_km REAL NOT NULL CHECK (length_km > 0),
    points_count INTEGER NOT NULL CHECK (points_count >= 2),
    description TEXT,  -- допускает NULL: описание может отсутствовать
    FOREIGN KEY (interest_id) REFERENCES interests(id)
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY,
    route_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    score REAL NOT NULL DEFAULT 1.0 CHECK (score BETWEEN 0 AND 1),
    is_dismissed INTEGER NOT NULL DEFAULT 0 CHECK (is_dismissed IN (0, 1)),
    FOREIGN KEY (route_id) REFERENCES routes(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
