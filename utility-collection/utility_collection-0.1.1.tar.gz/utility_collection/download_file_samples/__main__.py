import concurrent.futures
import os
import urllib.parse

import click
import rich.progress

from . import settings
from utility_collection.common.download import schedule_download


def prepare_files(data: list | dict | str) -> list[str]:
    if isinstance(data, dict):
        res: list[str] = []
        for key, value in data.items():
            files: list[str] = prepare_files(data=value)
            res += [os.path.join(key, file) for file in files]
        return res
    elif isinstance(data, list):
        res: list[str] = sum([prepare_files(data=x) for x in data], start=[])
        return res
    elif isinstance(data, str):
        return [data]
    else:
        return data


@click.command(name="download-file-samples")
@click.option("-p", "--prefix", type=click.Path())
def main(prefix: str = os.getcwd()):
    progress = rich.progress.Progress(
        rich.progress.TextColumn("[bold blue]{task.description}"),
        rich.progress.BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        rich.progress.DownloadColumn(),
        rich.progress.TransferSpeedColumn(),
        rich.progress.TimeRemainingColumn(),
    )

    files: list[str] = prepare_files(data=settings.SAMPLES)
    urls: list[str] = [
        urllib.parse.urljoin(base="https://filesamples.com/samples/", url=file)
        for file in files
    ]
    files: list[str] = [os.path.join(prefix, file) for file in files]
    with progress:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            for url, file in zip(urls, files):
                schedule_download(url=url, file=file, progress=progress, pool=pool)


if __name__ == "__main__":
    main()
