from contextlib import contextmanager, redirect_stdout
import time

exec_time = {}


@contextmanager
def timed(name: str = "", /, *, print_time: bool = False) -> None:
    global exec_time

    start = time.perf_counter_ns()
    yield
    end = time.perf_counter_ns()

    runtime = (end - start) / 10 ** 6
    if name:
        exec_time[name] = runtime
    if print_time:
        print(name, "took:", runtime, "ms")


@contextmanager
def stdout_to(filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        with redirect_stdout(file):
            yield
