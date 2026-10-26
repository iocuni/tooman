import json
from pathlib import Path
from tooman.config import prj_file, lock_file, pkg_dir
from tooman.exceptions import ToomanError

def init() -> None:
    root = Path.cwd()
    path = prj_file(root)

    if path.exists():
        raise ToomanError("package.json already exists.")

    name = root.name.lower().replace(" ", "-")
    prj = {"name": name, "version": "0.1.0", "type": "module", "dependencies": {}}
    path.write_text(json.dumps(prj, indent = 2, ensure_ascii = False) + "\n", encoding = "utf-8")
    lock_file(root).write_text(json.dumps({"lockfileVersion": 1, "packages": {}}, indent = 2) + "\n", encoding = "utf-8")
    pkg_dir(root).mkdir(parents=True, exist_ok=True)