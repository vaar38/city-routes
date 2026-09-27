-- Тестовые данные и примеры запросов (выполнять после schema.sql)

-- ==========================================================
-- Тестовые данные
-- ==========================================================

INSERT INTO users (name, email, password_hash, role) VALUES
    ('Анна',  'anna@example.com',  '$2b$12$exampleHashAnna.........................', 'user'),
    ('Борис', 'boris@example.com', '$2b$12$exampleHashBoris........................', 'user'),
    ('Admin', 'admin@example.com', '$2b$12$exampleHashAdmin........................', 'admin');

INSERT INTO interests (name) VALUES ('История'), ('Парки'), ('Архитектура'), ('Кафе');

INSERT INTO places (name, address, latitude, longitude) VALUES
    ('Красная площадь',  'Москва, Красная пл.',     55.753930, 37.620795),
    ('Парк Зарядье',     'Москва, ул. Варварка, 6', 55.751244, 37.628423),
    ('Парк Горького',    'Москва, ул. Крымский Вал, 9', 55.729823, 37.603080),
    ('Храм Христа Спасителя', 'Москва, ул. Волхонка, 15', 55.744600, 37.605500);

INSERT INTO routes (title, description, city, length_km, duration_min, author_id) VALUES
    ('Исторический центр', 'Главные достопримечательности центра', 'Москва', 3.20, 90, 3),
    ('Зелёная Москва',     'Прогулка по паркам',                    'Москва', 5.50, 120, 3);

INSERT INTO route_points (route_id, position, place_id) VALUES
    (1, 1, 1), (1, 2, 2), (1, 3, 4),
    (2, 1, 2), (2, 2, 3);

INSERT INTO route_interests (route_id, interest_id) VALUES (1, 1), (1, 3), (2, 2);
INSERT INTO user_interests  (user_id, interest_id)  VALUES (1, 1), (1, 3), (2, 2);

INSERT INTO reviews (user_id, route_id, rating, comment) VALUES
    (1, 1, 5, 'Отличный маршрут'),
    (2, 1, 4, 'Много людей, но интересно'),
    (2, 2, 5, NULL);

INSERT INTO favorites (user_id, route_id) VALUES (1, 1), (2, 2);

-- ==========================================================
-- Примеры запросов
-- ==========================================================

-- 1. Маршрут с точками по порядку
SELECT rp.position, p.name, p.latitude, p.longitude
FROM route_points rp
JOIN places p ON p.id = rp.place_id
WHERE rp.route_id = 1
ORDER BY rp.position;

-- 2. Рекомендации: маршруты, совпадающие с интересами пользователя,
--    сортировка по числу совпавших интересов, затем по рейтингу
SELECT r.id, r.title, COUNT(*) AS matched_interests, r.rating_avg
FROM user_interests ui
JOIN route_interests ri ON ri.interest_id = ui.interest_id
JOIN routes r           ON r.id = ri.route_id
WHERE ui.user_id = 1
GROUP BY r.id
ORDER BY matched_interests DESC, r.rating_avg DESC
LIMIT 10;

-- 3. Сохранение результата рекомендаций (score нормирован в [0; 1])
INSERT INTO recommendations (user_id, route_id, score)
SELECT ui.user_id, ri.route_id,
       ROUND(COUNT(*)::numeric / (SELECT COUNT(*) FROM user_interests WHERE user_id = 1), 3)
FROM user_interests ui
JOIN route_interests ri ON ri.interest_id = ui.interest_id
WHERE ui.user_id = 1
GROUP BY ui.user_id, ri.route_id;

-- 4. Рейтинг маршрутов — берётся из денормализованных полей, без AVG по reviews
SELECT title, rating_avg, reviews_count FROM routes ORDER BY rating_avg DESC;

-- 5. Проверка использования индекса
EXPLAIN SELECT * FROM routes WHERE city = 'Москва';
