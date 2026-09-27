-- Система рекомендаций городских маршрутов — схема БД (PostgreSQL)
-- Порядок создания: сначала независимые таблицы, затем таблицы с внешними ключами.

-- ==========================================================
-- 1. Основные сущности
-- ==========================================================

CREATE TABLE users (
    id            INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,              -- только хэш (bcrypt/argon2), не пароль
    role          VARCHAR(20)  NOT NULL DEFAULT 'user'
                  CHECK (role IN ('user', 'admin')),  -- «Гость» не хранится: это незарегистрированный посетитель
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CHECK (email LIKE '%_@_%')
);

CREATE TABLE interests (
    id   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE places (
    id        INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name      VARCHAR(200) NOT NULL,
    address   VARCHAR(300),
    latitude  NUMERIC(9, 6) NOT NULL CHECK (latitude  BETWEEN -90  AND 90),
    longitude NUMERIC(9, 6) NOT NULL CHECK (longitude BETWEEN -180 AND 180)
);

CREATE TABLE routes (
    id            INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title         VARCHAR(200) NOT NULL,
    description   TEXT,
    city          VARCHAR(100) NOT NULL,
    length_km     NUMERIC(6, 2) NOT NULL CHECK (length_km > 0),
    duration_min  INT           NOT NULL CHECK (duration_min > 0),
    author_id     INT REFERENCES users (id) ON DELETE SET NULL,  -- маршрут остаётся, даже если автор удалён
    created_at    TIMESTAMPTZ   NOT NULL DEFAULT now(),
    -- денормализация (см. README, раздел 5): агрегаты по отзывам, обновляются триггером
    rating_avg    NUMERIC(3, 2) NOT NULL DEFAULT 0 CHECK (rating_avg BETWEEN 0 AND 5),
    reviews_count INT           NOT NULL DEFAULT 0 CHECK (reviews_count >= 0)
);

-- ==========================================================
-- 2. Связи M:N
-- ==========================================================

CREATE TABLE route_points (
    route_id INT      NOT NULL REFERENCES routes (id) ON DELETE CASCADE,
    position SMALLINT NOT NULL CHECK (position >= 1),
    place_id INT      NOT NULL REFERENCES places (id) ON DELETE RESTRICT,  -- нельзя удалить место, пока оно в маршруте
    PRIMARY KEY (route_id, position)
);

CREATE TABLE user_interests (
    user_id     INT NOT NULL REFERENCES users (id)     ON DELETE CASCADE,
    interest_id INT NOT NULL REFERENCES interests (id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, interest_id)
);

CREATE TABLE route_interests (
    route_id    INT NOT NULL REFERENCES routes (id)    ON DELETE CASCADE,
    interest_id INT NOT NULL REFERENCES interests (id) ON DELETE CASCADE,
    PRIMARY KEY (route_id, interest_id)
);

CREATE TABLE favorites (
    user_id    INT         NOT NULL REFERENCES users (id)  ON DELETE CASCADE,
    route_id   INT         NOT NULL REFERENCES routes (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, route_id)
);

-- ==========================================================
-- 3. Отзывы и рекомендации
-- ==========================================================

CREATE TABLE reviews (
    id         INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id    INT         NOT NULL REFERENCES users (id)  ON DELETE CASCADE,
    route_id   INT         NOT NULL REFERENCES routes (id) ON DELETE CASCADE,
    rating     SMALLINT    NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment    TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, route_id)  -- один отзыв от пользователя на маршрут
);

CREATE TABLE recommendations (
    id         INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id    INT           NOT NULL REFERENCES users (id)  ON DELETE CASCADE,
    route_id   INT           NOT NULL REFERENCES routes (id) ON DELETE CASCADE,
    score      NUMERIC(4, 3) NOT NULL CHECK (score BETWEEN 0 AND 1),
    created_at TIMESTAMPTZ   NOT NULL DEFAULT now()
);

-- ==========================================================
-- 4. Индексы
-- PK и UNIQUE индексируются автоматически. Внешние ключи в PostgreSQL
-- автоматически НЕ индексируются — добавляем индексы под частые запросы.
-- ==========================================================

CREATE INDEX idx_routes_city            ON routes (city);                    -- поиск маршрутов по городу
CREATE INDEX idx_routes_author          ON routes (author_id);               -- «мои маршруты»
CREATE INDEX idx_route_points_place     ON route_points (place_id);          -- в каких маршрутах есть место
CREATE INDEX idx_route_interests_int    ON route_interests (interest_id);    -- маршруты по интересу (рекомендации)
CREATE INDEX idx_user_interests_int     ON user_interests (interest_id);     -- пользователи по интересу
CREATE INDEX idx_reviews_route          ON reviews (route_id, created_at DESC);         -- отзывы маршрута, новые сверху
CREATE INDEX idx_recommendations_user   ON recommendations (user_id, created_at DESC);  -- последние рекомендации пользователя
CREATE INDEX idx_recommendations_route  ON recommendations (route_id);
CREATE INDEX idx_favorites_route        ON favorites (route_id);             -- сколько раз маршрут в избранном

-- ==========================================================
-- 5. Триггер: пересчёт rating_avg и reviews_count при изменении отзывов
-- ==========================================================

CREATE FUNCTION refresh_route_rating() RETURNS TRIGGER AS $$
DECLARE
    r_id INT := COALESCE(NEW.route_id, OLD.route_id);
BEGIN
    UPDATE routes
    SET rating_avg    = COALESCE((SELECT ROUND(AVG(rating), 2) FROM reviews WHERE route_id = r_id), 0),
        reviews_count = (SELECT COUNT(*) FROM reviews WHERE route_id = r_id)
    WHERE id = r_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reviews_rating
AFTER INSERT OR UPDATE OF rating OR DELETE ON reviews
FOR EACH ROW EXECUTE FUNCTION refresh_route_rating();
