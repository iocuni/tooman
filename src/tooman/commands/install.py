from pathlib import Path
from tooman.core.project import find_prj
from tooman.core.installer import install as install_pkg

def install(name: str) -> str:
    return install_pkg(find_prj(Path.cwd()), name)