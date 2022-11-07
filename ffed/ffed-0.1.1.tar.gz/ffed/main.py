import click

from ffed import (
    EncoderEnum,
    HashesEnum,
    add_dynamic_docstring,
    mutually_exclusive_options,
)

from .adapter import FFED_Adapter


def encode_decode_help_section():
    """
    generate docstring for encode decode subcommand
    """
    help_section = f"available algo: {', '.join([algo.name for algo in EncoderEnum])}\n"

    return help_section


def hash_help_section():
    """
    generate docstring for hash subcommand
    """
    help_section = f"available algo: {', '.join([algo.name for algo in HashesEnum])}"

    return help_section


verbose_option = click.option(
    "-v", "--verbose", default=0, count=True, help="for verbosity"
)
input_from_stdin = click.option(
    "-in", "--stdin", default=False, is_flag=True, help="take input from stdin"
)
input_from_file = click.option("--file", type=str, help="take input from file")

output_to_file = click.option("--out", type=str, help="store the output to a file")

ffed_adapter = FFED_Adapter()


@click.group()
def cli():
    pass


@cli.command()
@verbose_option
@input_from_stdin
@input_from_file
@output_to_file
@click.option(
    "--algo", "algo", multiple=True, help="eg. --algo base64 or --algo base64,url"
)
@click.argument("string", required=False)
@add_dynamic_docstring(encode_decode_help_section)
@mutually_exclusive_options("stdin", "file", "string")
def encode(verbose, algo, out, **input_options):
    algo = [j for i in algo for j in i.split(",")]
    ret_value = ffed_adapter.encode(verbose, algo, out, **input_options)

    if ret_value:
        click.echo(ret_value)
        return ret_value

    click.echo(f"Output written in the file {out}")


@cli.command()
@verbose_option
@input_from_stdin
@input_from_file
@output_to_file
@click.option(
    "--algo", "algo", multiple=True, help="eg. --algo base64 or --algo base64,url"
)
@click.argument("string", required=False)
@add_dynamic_docstring(encode_decode_help_section)
@mutually_exclusive_options("stdin", "file", "string")
def decode(verbose, algo, out, **input_options):
    algo = [j for i in algo for j in i.split(",")]
    ret_value = ffed_adapter.decode(verbose, algo, out, **input_options)

    if ret_value:
        click.echo(ret_value)
        return ret_value

    click.echo(f"Output written in the file {out}")


@cli.command()
@verbose_option
@input_from_stdin
@input_from_file
@output_to_file
@click.option("--algo", "algo", multiple=True, help="eg. --algo md5 or --algo md5,sha1")
@click.argument("string", required=False)
@add_dynamic_docstring(hash_help_section)
@mutually_exclusive_options("stdin", "file", "string")
def hash(verbose, algo, out, **input_options):
    algo = [j for i in algo for j in i.split(",")]
    ret_value = ffed_adapter.hash(verbose, algo, out, **input_options)

    if ret_value:
        click.echo(ret_value)
        return ret_value

    click.echo(f"Output written in the file {out}")
