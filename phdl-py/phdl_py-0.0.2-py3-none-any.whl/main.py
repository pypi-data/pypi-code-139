import re
import time
from typing import List, Optional
from pathlib import Path

import typer
from rich import print
from tqdm.auto import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from phdl_py import __version__
from .utils import (setup_driver, get_url_m3u8, get_name,
                    download_m3u8_to_mp4, get_info_video, logger)


app = typer.Typer(name="phdl",
                  help="CLI to download videos.")


def callback_version(ctx: typer.Context, value: bool):
    """Print the version of this package."""
    if ctx.resilient_parsing:
        return

    if value:
        print(f"[cyan bold]Version:[/] [yellow bold]{__version__}[/]")
        raise typer.Exit()


@app.command(help="CLI to download videos.")
def run(urls: List[str] = typer.Argument(None,
                                         help="URLs to download.",
                                         show_default=False),
        dir_name: Optional[Path] = typer.Option("pornhub/",
                                                "-d",
                                                "--destination",
                                                help="Destination to save the downloaded videos.",
                                                show_default=False,
                                                rich_help_panel="CLI Options"),
        files_urls: typer.FileText = typer.Option(None,
                                                  "-f",
                                                  "--files-urls",
                                                  help="File with urls.",
                                                  rich_help_panel="CLI Options",
                                                  show_default=False),
        overwrite: bool = typer.Option(False,
                                       "-w",
                                       "--overwrite",
                                       help="Overwrite all already downloaded video.",
                                       show_default=False,
                                       rich_help_panel="CLI Options"),
        version: bool = typer.Option(False,
                                     "-v",
                                     "--version",
                                     help="Return the version of xvdl package.",
                                     show_default=False,
                                     callback=callback_version,
                                     is_eager=True,
                                     rich_help_panel="CLI Options")
        ):
    with logging_redirect_tqdm(loggers=[logger]):
        logger.info("Start new download!")
        # Instanciamos el driver de selenium
        driver = setup_driver()

        # En caso de pasar un archivo con urls, pasamos esa lista a la variable urls
        if files_urls:
            urls = list(map(lambda x: x.strip(), files_urls.readlines()))

        # Nos aseguramos que la variable urls no venga vacia
        assert urls, typer.BadParameter("No urls were provided.")

        # Nos aseguramos que el directorio de descarga exista
        dir_name.mkdir(parents=True, exist_ok=True)

        # Creamos un string con el nombre de todos archivos previamente descargados
        name_files = map(lambda x: x.name, dir_name.glob("*"))
        name_files = " ".join(name_files)

        # Comenzamos con el loop de descarga
        for idx, url in enumerate(tqdm(urls, colour="green"), start=1):
            logger.info(f"{idx}/{len(urls)}.- Request to {url}")

            # Obtenemos el video id a partir de la url
            video_id = re.search("(?<==)ph\w+", url).group(0)

            # Verificamos que el video id no este entre los archivos ya descargados
            if not video_id in name_files or overwrite:
                # Hacemos la request a la url y obtenemos el url del m3u8 del video
                url_m3u8 = get_url_m3u8(driver, url)

                # Obtenemos el nombre del video
                name = get_name(driver)

                # Construimos el nombre del archivo que se descargará
                filename = dir_name / f"{name}{video_id}.mp4"

                # Invocamos la función que se encargará de la descarga.
                download_m3u8_to_mp4(url_m3u8, filename, overwrite)

            else:
                # Si el video ya fue descargado antes, se salta esa url,
                # pero se imprime la info del archivo.
                filename = list(dir_name.glob(f"*{video_id}*"))[0]
                logger.warning(f"SKIP! {filename} was already downloaded.")
                logger.info(get_info_video(filename))
                time.sleep(0.1)

        # Se cierra el driver se selenium
        driver.close()
        logger.info("Finished download!\n")


if __name__ == '__main__':
    app()
