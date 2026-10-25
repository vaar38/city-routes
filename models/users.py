"""Класс User и функции работы с коллекцией пользователей."""

from .routes import next_id


class User:
    """Пользователь системы с одним основным интересом."""

    def __init__(self, user_id: int, name: str, email: str, interest: str) -> None:
        """Создать пользователя. Проверки перенесены из add_user() ПР2."""
        if not name.strip():
            raise ValueError("Имя пользователя не указано")
        if "@" not in email:
            raise ValueError("Некорректный адрес электронной почты")
        if not interest.strip():
            raise ValueError("Интерес не указан")
        self.id = user_id
        self.name = name.strip()
        self.email = email.strip()
        self.interest = interest.strip().lower()

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря, прочитанного из JSON."""
        return cls(data["id"], data["name"], data["email"], data["interest"])

    def change_interest(self, interest: str) -> None:
        """Изменить интерес пользователя."""
        if not interest.strip():
            raise ValueError("Интерес не указан")
        self.interest = interest.strip().lower()

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>, интерес: {self.interest}"


def add_user(users: list[User], name: str, email: str, interest: str) -> User:
    """Создать объект User и добавить его в коллекцию."""
    user = User(next_id(users), name, email, interest)
    users.append(user)
    return user


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по подстроке имени или адреса почты."""
    query = query.strip().lower()
    return [
        user for user in users
        if query in user.name.lower() or query in user.email.lower()
    ]


def change_interest(users: list[User], user_id: int, interest: str) -> bool:
    """Найти пользователя и изменить его интерес методом User.change_interest()."""
    user = find_user_by_id(users, user_id)
    if user is None or not interest.strip():
        return False
    user.change_interest(interest)
    return True


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователей нет.")
        return
    for user in users:
        print(f"{user.id:>3}  {user}")
