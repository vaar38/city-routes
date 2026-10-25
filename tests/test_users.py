import pytest

from users import add_user, change_interest, find_user


def test_add_user():
    users = []
    user = add_user(users, "Артур", "artur@example.com", "Архитектура")
    assert user["id"] == 1
    assert user["interest"] == "архитектура"


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
    assert users[0]["interest"] == "стрит-арт"
    assert not change_interest(users, 99, "парки")
