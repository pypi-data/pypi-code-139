import os
from pathlib import Path

import click
from click import BadParameter


@click.group
def main():
    pass


@main.command()
@click.argument("project_name")
@click.argument("path", type=click.Path(exists=True), default=".")
def startapiprojct(project_name, path):
    """create project directories."""
    if Path(path).is_dir():
        project_path = Path(
            os.path.abspath(os.path.join(Path.cwd(), path)) + "/" + project_name
        )
        project_path.mkdir(parents=True, exist_ok=True)
        (project_path / "__init__.py").touch()
        (project_path / f"{project_name}.py").touch()

    else:
        raise BadParameter(
            f"{os.path.abspath(os.path.join(Path.cwd(), path))} is a file, not directory.",
            param_hint="[PATH]",
        )


if __name__ == "__main__":
    main()
