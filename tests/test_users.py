import pytest

from models import User
from models.users import add_user, change_interest, find_user


def test_user_creation():
    user = User(1, "Артур", "artur@example.com", "Архитектура")
    assert user.name == "Артур"
    assert user.interest == "архитектура"
    assert "artur@example.com" in str(user)


def test_user_from_data():
    data = {"id": 2, "name": "Анна", "email": "anna@example.com", "interest": "парки"}
    user = User.from_data(data)
    assert user.id == 2


def test_add_user():
    users = []
    user = add_user(users, "Артур", "artur@example.com", "Архитектура")
    assert user.id == 1
    assert users == [user]


def test_add_user_bad_email():
    with pytest.raises(ValueError):
        add_user([], "Артур", "без-почты", "парки")


def test_find_user_by_email():
    users = []
    add_user(users, "Анна", "anna@example.com", "парки")
    assert find_user(users, "ANNA@")


def test_change_interest():
    users = []
    add_user(users, "Анна", "anna@example.com", "парки")
    assert change_interest(users, 1, "Стрит-арт")
    assert users[0].interest == "стрит-арт"
    assert not change_interest(users, 99, "парки")
