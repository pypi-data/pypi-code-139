import concurrent.futures
import os

import requests
import rich.progress


def download(
    url: str, file: str, progress: rich.progress.Progress, task_id: rich.progress.TaskID
):
    res: requests.Response = requests.get(url=url, stream=True)
    total: int = int(res.headers.get("Content-Length", default=0))
    progress.update(task_id=task_id, total=(total if total else None))
    os.makedirs(name=os.path.dirname(p=file), exist_ok=True)
    with open(file=file, mode="wb") as fp:
        progress.start_task(task_id=task_id)
        for chunk in res.iter_content(chunk_size=1024 * 1024):
            bytes_written: int = fp.write(chunk)
            progress.advance(task_id=task_id, advance=bytes_written)
        if not total:
            progress.update(task_id=task_id, total=fp.tell())
    progress.stop_task(task_id=task_id)


def schedule_download(
    url: str,
    file: str,
    progress: rich.progress.Progress,
    pool: concurrent.futures.Executor,
):
    task_id: rich.progress.TaskID = progress.add_task(
        description=file, start=False, total=None
    )
    pool.submit(download, url=url, file=file, progress=progress, task_id=task_id)
