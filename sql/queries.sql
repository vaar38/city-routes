-- ==========================================
-- City Routes: SQL-запросы проекта
-- ==========================================
-- Литералы (5, 'парки', 1 ...) — значения для проверки в SQLite CLI.
-- В Django-представлениях на их месте стоят параметры ?.
-- Вид запроса указан в скобках: [список], [WHERE], [JOIN], [агрегат], [GROUP BY], [HAVING].


-- 1. [список][JOIN] Список маршрутов с тематикой, по названию.
--    Страница /routes/.
SELECT
    routes.id,
    routes.name,
    interests.name AS interest,
    routes.length_km,
    routes.points_count
FROM routes
JOIN interests ON routes.interest_id = interests.id
ORDER BY routes.name;


-- 2. [список] Список пользователей по имени.
--    Выпадающий список на странице /recommendations/pick/.
SELECT
    id,
    name,
    email
FROM users
ORDER BY name;


-- 3. [список] Список тематик.
--    Выпадающий список на странице /routes/search/.
SELECT
    id,
    name
FROM interests
ORDER BY name;


-- 4. [WHERE] Короткие маршруты: не длиннее 5 км, от коротких к длинным.
SELECT
    id,
    name,
    length_km
FROM routes
WHERE length_km <= 5
ORDER BY length_km;


-- 5. [WHERE][JOIN] Поиск маршрутов по тематике и максимальной длине.
--    Страница /routes/search/?interest=парки&max_km=5.
--    Пустая тематика или пустая длина = «без ограничения».
SELECT
    routes.id,
    routes.name,
    interests.name AS interest,
    routes.length_km,
    routes.points_count
FROM routes
JOIN interests ON routes.interest_id = interests.id
WHERE ('парки' = '' OR interests.name = 'парки')
  AND (5 IS NULL OR routes.length_km <= 5)
ORDER BY routes.length_km;


-- 6. [WHERE][JOIN] Карточка маршрута по id.
--    Страница /routes/1/.
SELECT
    routes.id,
    routes.name,
    interests.name AS interest,
    routes.length_km,
    routes.points_count,
    routes.description
FROM routes
JOIN interests ON routes.interest_id = interests.id
WHERE routes.id = 1;


-- 7. [WHERE][JOIN] Кому активно рекомендован маршрут 1.
--    Блок на странице /routes/1/.
SELECT
    users.name AS user_name,
    recommendations.score
FROM recommendations
JOIN users ON recommendations.user_id = users.id
WHERE recommendations.route_id = 1
  AND recommendations.is_dismissed = 0
ORDER BY recommendations.score DESC;


-- 8. [WHERE][JOIN] Активные рекомендации: данные из трёх таблиц вместо id.
--    Страница /recommendations/.
SELECT
    recommendations.id,
    users.name AS user_name,
    routes.id AS route_id,
    routes.name AS route_name,
    routes.length_km,
    recommendations.score
FROM recommendations
JOIN users ON recommendations.user_id = users.id
JOIN routes ON recommendations.route_id = routes.id
WHERE recommendations.is_dismissed = 0
ORDER BY users.name, recommendations.score DESC;


-- 9. [JOIN] Полная информация об одной рекомендации (четыре таблицы).
--    Страница /recommendations/2/.
SELECT
    recommendations.id,
    recommendations.score,
    recommendations.is_dismissed,
    users.name AS user_name,
    users.email,
    routes.id AS route_id,
    routes.name AS route_name,
    routes.length_km,
    interests.name AS interest
FROM recommendations
JOIN users ON recommendations.user_id = users.id
JOIN routes ON recommendations.route_id = routes.id
JOIN interests ON routes.interest_id = interests.id
WHERE recommendations.id = 2;


-- 10. [WHERE][JOIN] Подбор: маршруты по интересу пользователя 4,
--     которые ему ещё не рекомендованы (подзапрос NOT IN).
--     Отклонённая рекомендация (маршрут 4) не мешает подбору.
--     Страница /recommendations/pick/?user=4.
SELECT
    routes.id,
    routes.name,
    routes.length_km
FROM routes
JOIN users ON users.interest_id = routes.interest_id
WHERE users.id = 4
  AND routes.id NOT IN (
      SELECT route_id
      FROM recommendations
      WHERE user_id = 4
        AND is_dismissed = 0
  )
ORDER BY routes.length_km;


-- 11. [агрегат] Сводка по маршрутам: количество, средняя / минимальная /
--     максимальная длина, сумма точек. Страница /recommendations/statistics/.
SELECT
    COUNT(*) AS routes_count,
    ROUND(AVG(length_km), 1) AS avg_length,
    MIN(length_km) AS min_length,
    MAX(length_km) AS max_length,
    SUM(points_count) AS points_total
FROM routes;


-- 12. [агрегат][WHERE] Количество активных рекомендаций.
--     Главная страница и статистика.
SELECT
    COUNT(*) AS active_count
FROM recommendations
WHERE is_dismissed = 0;


-- 13. [GROUP BY][JOIN] Маршруты по тематикам: количество и средняя длина.
--     LEFT JOIN оставляет тематики без маршрутов (COUNT вернёт 0).
SELECT
    interests.name AS interest,
    COUNT(routes.id) AS routes_count,
    ROUND(AVG(routes.length_km), 1) AS avg_length
FROM interests
LEFT JOIN routes ON routes.interest_id = interests.id
GROUP BY interests.id, interests.name
ORDER BY routes_count DESC, interest;


-- 14. [GROUP BY][JOIN] Активные рекомендации по маршрутам и средняя релевантность.
--     Условие is_dismissed = 0 стоит в ON, чтобы маршруты без
--     рекомендаций не пропали из LEFT JOIN.
SELECT
    routes.id,
    routes.name AS route_name,
    COUNT(recommendations.id) AS recs_count,
    ROUND(AVG(recommendations.score), 2) AS avg_score
FROM routes
LEFT JOIN recommendations
    ON recommendations.route_id = routes.id
   AND recommendations.is_dismissed = 0
GROUP BY routes.id, routes.name
ORDER BY recs_count DESC, route_name;


-- 15. [GROUP BY][JOIN] Рекомендации по пользователям: всего и отклонённых.
SELECT
    users.name AS user_name,
    COUNT(recommendations.id) AS total,
    SUM(recommendations.is_dismissed) AS dismissed
FROM users
LEFT JOIN recommendations ON recommendations.user_id = users.id
GROUP BY users.id, users.name
ORDER BY total DESC, user_name;


-- 16. [GROUP BY][HAVING] Популярные маршруты: активных рекомендаций больше 1.
--     WHERE отбрасывает отклонённые записи до группировки,
--     HAVING — группы после подсчёта.
SELECT
    routes.id,
    routes.name AS route_name,
    COUNT(recommendations.id) AS recs_count
FROM routes
JOIN recommendations ON recommendations.route_id = routes.id
WHERE recommendations.is_dismissed = 0
GROUP BY routes.id, routes.name
HAVING COUNT(recommendations.id) > 1
ORDER BY recs_count DESC;


-- 17. [GROUP BY][LIMIT] Три самых рекомендуемых маршрута.
SELECT
    routes.name AS route_name,
    COUNT(recommendations.id) AS recs_count
FROM routes
JOIN recommendations ON recommendations.route_id = routes.id
WHERE recommendations.is_dismissed = 0
GROUP BY routes.id, routes.name
ORDER BY recs_count DESC, route_name
LIMIT 3;
