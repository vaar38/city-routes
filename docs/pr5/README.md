# Практическая работа № 5

**Дисциплина:** Технологии разработки приложений на базе фреймворков
**Тема:** Django, HTTP и основы веб-разработки
**Студент:** Ватаншоев Артур Бахтоваршоевич, группа ЭФБО-08-24
**Проект:** Система рекомендаций городских маршрутов (№408)
**Год:** 2026

## 1. Выполненные материалы Яндекс Практикума

| Раздел | Выполненная тема |
|---|---|
| 04. «Основы веб-разработки» | «Создание проекта» |
| | «Пути и view-функции» |
| | «Вёрстка для бэкендера» |

## 2. Доработка индивидуального проекта

**Репозиторий:** https://github.com/vaar38/city-routes

- Django 5.2 добавлен в `requirements.txt` (`Django==5.2.*`) и установлен в `.venv`.
- Django-проект `city_routes` создан в корне репозитория (`django-admin startproject city_routes .`), рядом с кодом ПР1–ПР3. Настроены `LANGUAGE_CODE = "ru-RU"`, `TIME_ZONE = "Europe/Moscow"`, `ALLOWED_HOSTS`.
- Приложения `homepage`, `routes`, `recommendations` созданы и зарегистрированы в `INSTALLED_APPS`. Отдельное приложение для пользователей не создавалось: у Django есть встроенный `User`, аутентификация будет позже.
- Маршрутизация двух уровней: корневой `city_routes/urls.py` подключает `urls.py` приложений через `include()`.

| URL | View-функция | Результат |
|---|---|---|
| `/` | `homepage.views.index` | главная страница |
| `/routes/` | `routes.views.routes` | список маршрутов (сортировка `sort_routes()`) |
| `/routes/<int:route_id>/` | `routes.views.route_detail` | карточка маршрута; бейдж «короткая/длинная прогулка» через `Route.is_suitable_for()`; 404, если маршрута нет |
| `/recommendations/` | `recommendations.views.recommendations` | список рекомендаций, статусы-бейджи |
| `/recommendations/<int:rec_id>/` | `recommendations.views.recommendation_detail` | карточка рекомендации: данные из связанных объектов `rec.user`, `rec.route`; 404, если нет |

- Общий HTML-каркас — функция `page()` в `homepage/views.py` (Bootstrap 5.3 через CDN, навигация, `container`).
- Собственная страница 404: `handler404 = "homepage.views.page_not_found"` в корневом `urls.py`, проверена при `DEBUG = False`.
- Данные по-прежнему в JSON: view-функции используют `load_routes()`, `load_users()`, `load_recommendations()`, `find_route_by_id()`, `find_recommendation_by_id()` из ПР3. Консольная версия `main.py` сохранена.

## 3. Результат работы

- создан Django-проект и три приложения, подключённых к проекту;
- настроена маршрутизация, динамические URL с конвертером `<int:...>`, обработка 404;
- реализованы view-функции и пять страниц, навигация между ними;
- использованы HTML и Bootstrap;
- предметная область ПР3 отображается в веб-интерфейсе.

**Проверки:** `python manage.py check` — без замечаний; `pytest -v` — 27 тестов проходят; `flake8 . --extend-exclude=venv` — без замечаний.

## 4. Вывод

Консольный проект получил веб-слой: запрос проходит цепочку URL → urls.py → view → HttpResponse, а данные берутся из объектной модели ПР3. HTML пока собирается в Python-строках — в ПР6 он будет перенесён в шаблоны Django.
