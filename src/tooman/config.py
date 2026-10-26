from pathlib import Path
ORGANIZATION = "tooman-packages"
PRJ_FILE = "package.json"
LOCK_FILE = "tooman.lock"
PACK_DIR = "tooman_packages"
GIT_TIMEOUT = 300

def prj_file(root: Path) -> Path:
    return root / PRJ_FILE

def lock_file(root: Path) -> Path:
    return root / LOCK_FILE

def pkg_dir(root: Path) -> Path:
    return root / PACK_DIR