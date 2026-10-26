import json
from pathlib import Path
from tooman.config import prj_file
from tooman.exceptions import ToomanError

def find_prj(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()

    for dir in (cur, *cur.parents):
        if prj_file(dir).is_file():
            return dir

    raise ToomanError("No package.json found.")

def read_prj(root: Path) -> dict:
    path = prj_file(root)

    try:
        data = json.loads(path.read_text(encoding = "utf-8"))
    except json.JSONDecodeError as e:
        raise ToomanError(f"Invalid package.json: {e}") from e

    if not isinstance(data, dict):
        raise ToomanError("package.json must contain an object.")

    data.setdefault("dependencies", {})
    return data

def write_prj(root: Path, data: dict) -> None:
    prj_file(root).write_text(json.dumps(data, indent = 2, ensure_ascii = False) + "\n", encoding = "utf-8")