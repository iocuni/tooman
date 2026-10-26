from pathlib import Path
from tooman.core.project import find_prj
from tooman.core.installer import update as update_pkgs

def update(name: str | None = None) -> list[tuple[str, str]]:
    return update_pkgs(find_prj(Path.cwd()), name)