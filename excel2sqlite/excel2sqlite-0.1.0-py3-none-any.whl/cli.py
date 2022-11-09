import typer
import pathlib
from .functions import *

app = typer.Typer()


@app.command()
def main(filename: pathlib.Path):

    if not filename.exists():
        print(f"Filename not found: {filename}")
        typer.Exit(1)

    output_filename = filename.parent / (filename.stem + ".db")

    excel2sqlite(filename,output_filename)
