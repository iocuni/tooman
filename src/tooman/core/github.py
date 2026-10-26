import re
import subprocess
from pathlib import Path
from tooman.config import GIT_TIMEOUT, ORGANIZATION
from tooman.exceptions import ToomanError

def check_name(name: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name) or name in (".", ".."):
        raise ToomanError(f"Invalid package name: {name}")

def repo_url(name: str) -> str:
    check_name(name)
    return f"https://github.com/{ORGANIZATION}/{name}.git"

def run_git(args: list[str], cwd: Path | None = None) -> str:
    try:
        result = subprocess.run(["git", *args], cwd = cwd, capture_output = True, text = True, check = True, timeout = GIT_TIMEOUT)
        return result.stdout.strip()
    except FileNotFoundError as e:
        raise ToomanError("Git is not installed.") from e
    except subprocess.TimeoutExpired as e:
        raise ToomanError("Git command timed out.") from e
    except subprocess.CalledProcessError as e:
        raise ToomanError(e.stderr.strip() or "Git command failed.") from e

def clone_repo(name: str, target: Path) -> str:
    run_git(["clone", "--depth", "1", repo_url(name), str(target)])
    return run_git(["rev-parse", "HEAD"], target)

def update_repo(target: Path) -> str:
    if run_git(["status", "--porcelain"], target):
        raise ToomanError(f"Package has local changes: {target.name}")

    run_git(["pull", "--ff-only"], target)
    return run_git(["rev-parse", "HEAD"], target)