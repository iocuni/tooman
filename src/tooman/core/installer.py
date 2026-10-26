import shutil
from pathlib import Path
from tooman.config import pkg_dir
from tooman.exceptions import ToomanError
from tooman.core.project import read_prj, write_prj
from tooman.core.github import check_name, repo_url, clone_repo, update_repo
from tooman.core.lockfile import read_lock, write_lock

def install(root: Path, name: str) -> str:
    check_name(name)

    target = pkg_dir(root) / name
    prj = read_prj(root)
    lock = read_lock(root)

    if target.exists():
        raise ToomanError(f"Package already exists: {name}")

    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        commit = clone_repo(name, target)
    except Exception:
        if target.exists():
            shutil.rmtree(target)
        raise

    prj["dependencies"][name] = f"github:{name}"
    lock["packages"][name] = {"repository": repo_url(name), "path": str(target.relative_to(root)), "commit": commit}

    write_prj(root, prj)
    write_lock(root, lock)
    return commit

def remove(root: Path, name: str) -> None:
    check_name(name)

    target = pkg_dir(root) / name
    prj = read_prj(root)
    lock = read_lock(root)

    if not target.exists() and name not in prj["dependencies"]:
        raise ToomanError(f"Package not installed: {name}")

    if target.exists():
        if target.resolve().parent != pkg_dir(root).resolve():
            raise ToomanError(f"Invalid package path: {name}")
        shutil.rmtree(target)

    prj["dependencies"].pop(name, None)
    lock["packages"].pop(name, None)

    write_prj(root, prj)
    write_lock(root, lock)

def update(root: Path, name: str | None = None) -> list[tuple[str, str]]:
    prj = read_prj(root)
    lock = read_lock(root)
    names = [name] if name else list(prj["dependencies"])
    updated = []

    if name and name not in prj["dependencies"]:
        raise ToomanError(f"Package not installed: {name}")

    for pkg in names:
        check_name(pkg)
        target = pkg_dir(root) / pkg

        if not target.is_dir() or not (target / ".git").is_dir():
            raise ToomanError(f"Package not found: {pkg}")

        commit = update_repo(target)
        lock["packages"].setdefault(pkg, {})["commit"] = commit
        updated.append((pkg, commit))

    write_lock(root, lock)
    return updated

def list_installed(root: Path) -> list[tuple[str, str, bool]]:
    prj = read_prj(root)
    lock = read_lock(root)
    result = []

    for name in prj["dependencies"]:
        commit = lock["packages"].get(name, {}).get("commit", "unknown")
        installed = (pkg_dir(root) / name).is_dir()
        result.append((name, commit[:7], installed))

    return result