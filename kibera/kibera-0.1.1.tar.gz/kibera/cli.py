import logging
import os
import re
import signal
import sys
import threading

import click
import portforward

from kibera import keys, users
from kibera.core import db
from kibera.core.metrics import start_metrics_server

logger = logging.getLogger(__name__)


log_colors = (("uvicorn.*", 242),)


@click.group()
@click.option(
    "--log-level",
    default="info",
    type=click.Choice(
        ["debug", "info", "warning", "error", "critical"], case_sensitive=False
    ),
)
@click.option("--log-file", required=False, default=None)
@click.option("--redis", required=False, default="redis://127.0.0.1:6379")
@click.option("--mongo", required=False, default="mongodb://127.0.0.1:27017")
def cli(log_level, log_file, redis, mongo):
    from kibera.core.logging import init_logging

    init_logging(logging.getLevelName(log_level.upper()), log_file, colors=log_colors)
    db.set_url(mongo)


@cli.command()
@click.option("-p", "--port", default=8080)
@click.option("--metrics", required=False, default=9100)
def server(port, metrics):
    from waitress import serve

    from kibera.api import app

    def handler(signum, frame):
        print("Exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    start_metrics_server(metrics_port=metrics)
    serve(app, listen=f"*:{port}")


@cli.command()
@click.option(
    "-k",
    "--kubeconfig",
    default=os.getenv("KUBECONFIG", os.path.expanduser("~/.kube/config")),
)
@click.option("--namespace", default="kibera")
@click.option("--pod", default="mongodb-0")
@click.option("--src-port", default=27017)
@click.option("--dst-port", default=27017)
def connect(kubeconfig, namespace, pod, src_port, dst_port):
    if not os.path.exists(kubeconfig):
        print(f"Kubeconfig not found at '{kubeconfig}'")
        sys.exit(1)
    print("Using kubeconfig %s", kubeconfig)

    ctx = portforward.forward(
        namespace,
        pod,
        src_port,
        dst_port,
        config_path=kubeconfig,
        log_level=portforward.LogLevel.ERROR,
    )

    lock = threading.Lock()

    def handler(signum, frame):
        lock.release
        print("Exiting...")
        sys.exit(0)

    lock.acquire()
    with ctx:
        print(f"Forwarding port {src_port} to kube {namespace}/{pod}:{dst_port}")
        print("Ctrl-C to exit")
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)
        lock.acquire()


@cli.group()
def add():
    pass


@cli.group()
def update():
    pass


@cli.group()
def delete():
    pass


@cli.group()
def get():
    pass


@add.command(name="key")
@click.argument("data", nargs=-1)
def add_key(data):
    key = parse_key_arg(data)
    keys.create_key("root", key)
    keys.print_key(keys.get_key(key))


@update.command(name="key")
@click.argument("data", nargs=-1)
def update_key(data):
    key = parse_key_arg(data)
    keys.update_key("root", key)
    keys.print_key(keys.get_key(key))


@get.command(name="key")
@click.argument("query", nargs=-1)
def get_key(query):
    data = parse_key_arg(query)
    key = keys.get_key(data)
    if key is None:
        print("Key not found")
        return
    keys.print_key(key)


@get.command(name="keys")
@click.argument("query", nargs=-1)
def get_keys(query):
    data = parse_key_arg(query)
    keylist = keys.list_keys(data)
    keys.print_key(list(keylist))


@delete.command(name="key")
@click.argument("query", nargs=-1)
def delete_key(query):
    data = parse_key_arg(query)
    keys.delete_key("root", data)


@add.command(name="user")
@click.argument("name")
def add_user(name):
    users.create(name)
    users.print_user(users.get(name))


@get.command(name="user")
@click.argument("name")
def get_user(name):
    user = users.get(name)
    if user is None:
        print("User not found")
        return
    users.print_user(user)


@get.command(name="users")
def get_users():
    users.print_user(list(users.list()))


@cli.command()
def shell():
    from kibera.core.shell import start_shell

    start_shell(db=db)


def parse_key_arg(key_data):
    qre = re.compile("([a-zA-Z0-9_-]+)=([a-zA-Z0-9_-]*)?")

    key = {}

    for s in key_data:
        m = qre.match(s)
        if m is not None:
            k, v = m.groups()
            key[k] = v
        else:
            key.update(keys.parse_key_url(s))

    if key.get("port") is not None:
        key["port"] = int(key["port"])

    return key


def main():
    cli(auto_envvar_prefix="KIBERA")
