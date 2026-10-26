from pathlib import Path
from tooman.core.project import find_prj
from tooman.core.installer import remove as remove_pkg

def remove(name: str) -> None:
    remove_pkg(find_prj(Path.cwd()), name)