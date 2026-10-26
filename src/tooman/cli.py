import typer
from rich import print
from tooman.exceptions import ToomanError
from tooman.commands.init import init
from tooman.commands.install import install
from tooman.commands.remover import remove
from tooman.commands.update import update
from tooman.commands.list import list_pkgs

app = typer.Typer(no_args_is_help=True)

def run(fn, *args):
    try:
        return fn(*args)
    except ToomanError as e:
        print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

@app.command()
def init_cmd():
    run(init)
    print("[green]Initialized project.[/green]")

@app.command("install")
def install_cmd(name: str):
    commit = run(install, name)
    print(f"[green]Installed {name}[/green] ({commit[:7]})")

@app.command("remove")
def remove_cmd(name: str):
    run(remove, name)
    print(f"[green]Removed {name}[/green]")

@app.command("update")
def update_cmd(name: str | None = typer.Argument(default=None)):
    result = run(update, name)

    for pkg, commit in result:
        print(f"[green]Updated {pkg}[/green] ({commit[:7]})")

@app.command("list")
def list_cmd():
    result = run(list_pkgs)

    if not result:
        print("No packages installed.")
        return

    for name, commit, installed in result:
        status = "[green]installed[/green]" if installed else "[red]missing[/red]"
        print(f"{name} ({commit}) - {status}")

if __name__ == "__main__":
    app()