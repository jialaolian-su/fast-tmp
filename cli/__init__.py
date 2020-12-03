import typer
import sys

app = typer.Typer()
import os


@app.command()
def hello(name: str, aer: str = typer.Option(...,)):
    typer.echo(f"hello {name}")
    typer.secho(aer, color='green')


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


if __name__ == "__main__":
    app()
