"""Вспомогательные функции безопасного ввода."""


def input_int(prompt: str) -> int:
    """Запросить целое число; при ошибке повторить запрос."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить дробное число (допускается запятая); при ошибке повторить запрос."""
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Ошибка: введите число, например 4.5")


def input_text(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Ошибка: значение не может быть пустым.")
