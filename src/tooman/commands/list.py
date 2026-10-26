from pathlib import Path
from tooman.core.project import find_prj
from tooman.core.installer import list_installed

def list_pkgs() -> list[tuple[str, str, bool]]:
    return list_installed(find_prj(Path.cwd()))