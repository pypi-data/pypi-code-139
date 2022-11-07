import click

from ppcmd.ppc.params import TgzParam
from ppcmd.ppc.ppc_processor import PpcProcessor
from ppcmd.ppc.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

processor = PpcProcessor()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
def cli():
    """Pico Python Command"""


@cli.command()
@click.argument("src_dir", type=str)
@click.argument("out_dir", type=str, default='.')
@click.option("-o", "--outfile-name", default='',
              help="output file name prefix'. (default: out_dir basename)")
@click.option("-c", "--custom-timestamp-suffix", default='',
              help="YYMMDD_HHMMSS_***. (default: blank)")
@click.option("-p", "--prefix-timestamp", default=False, is_flag=True)
def tgz(src_dir, out_dir, outfile_name,
        prefix_timestamp, custom_timestamp_suffix):
    """Tgz dir."""
    tgz_param = TgzParam(src_dir, out_dir, outfile_name,
                         prefix_timestamp, custom_timestamp_suffix)
    processor.tgz(tgz_param)
