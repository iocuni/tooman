import json
from pathlib import Path
from tooman.config import lock_file

def read_lock(root: Path) -> dict:
    path = lock_file(root)

    if not path.is_file():
        return {"lockfileVersion": 1, "packages": {}}

    try:
        data = json.loads(path.read_text(encoding = "utf-8"))
    except json.JSONDecodeError:
        return {"lockfileVersion": 1, "packages": {}}

    if not isinstance(data, dict):
        return {"lockfileVersion": 1, "packages": {}}

    data.setdefault("lockfileVersion", 1)
    data.setdefault("packages", {})
    return data

def write_lock(root: Path, data: dict) -> None:
    lock_file(root).write_text(json.dumps(data, indent = 2, ensure_ascii = False) + "\n", encoding = "utf-8")