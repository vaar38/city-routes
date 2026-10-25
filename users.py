"""Функции работы с пользователями.

Пользователь хранится словарём:
{"id": 1, "name": "...", "email": "...", "interest": "..."}
"""

from routes import next_id


def add_user(users: list[dict], name: str, email: str, interest: str) -> dict:
    """Создать пользователя и добавить его в список users.

    Проверки перенесены из create_user() ПР1.
    """
    if not name.strip():
        raise ValueError("Имя пользователя не указано")
    if "@" not in email:
        raise ValueError("Некорректный адрес электронной почты")
    if not interest.strip():
        raise ValueError("Интерес не указан")

    user = {
        "id": next_id(users),
        "name": name.strip(),
        "email": email.strip(),
        "interest": interest.strip().lower(),
    }
    users.append(user)
    return user


def find_user_by_id(users: list[dict], user_id: int) -> dict | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def find_user(users: list[dict], query: str) -> list[dict]:
    """Найти пользователей по подстроке имени или адреса почты."""
    query = query.strip().lower()
    return [
        user for user in users
        if query in user["name"].lower() or query in user["email"].lower()
    ]


def change_interest(users: list[dict], user_id: int, interest: str) -> bool:
    """Изменить интерес пользователя (управление профилем)."""
    user = find_user_by_id(users, user_id)
    if user is None or not interest.strip():
        return False
    user["interest"] = interest.strip().lower()
    return True


def show_users(users: list[dict]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователей нет.")
        return
    for user in users:
        print(f"{user['id']:>3}  {user['name']:<20} {user['email']:<24} {user['interest']}")
