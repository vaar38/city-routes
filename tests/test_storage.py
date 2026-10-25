from storage import load_json, save_json


def test_save_and_load(tmp_path):
    path = tmp_path / "items.json"
    save_json(path, [{"id": 1, "name": "Центр"}])
    assert load_json(path) == [{"id": 1, "name": "Центр"}]


def test_missing_file(tmp_path):
    assert load_json(tmp_path / "nope.json") == []


def test_broken_file(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{oops", encoding="utf-8")
    assert load_json(path) == []
