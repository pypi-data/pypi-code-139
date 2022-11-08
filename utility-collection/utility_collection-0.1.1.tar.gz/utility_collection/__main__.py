import click

from .download_file_samples.__main__ import main as download_file_samples


@click.group(name="utility-collection")
def main():
    pass


main.add_command(cmd=download_file_samples)


if __name__ == "__main__":
    main()
