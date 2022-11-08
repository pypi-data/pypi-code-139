import os
from ssl import SSLContext, create_default_context

from gino import Gino
from gino.dialects.asyncpg import Pool
from sqlalchemy.engine.url import URL
from src.microservice.core.config import conf

db = Gino()


def import_models(apps_list=None):
    if apps_list is None:
        apps_list = []
    apps_dir = os.path.join(conf.BASE_DIR, "src", "apps")

    for app in os.listdir(apps_dir):
        if app.startswith("__"):
            continue
        if app not in apps_list:
            continue

        try:
            __import__("src.apps." + app + ".models")
        except ModuleNotFoundError as e:
            raise e


def get_bind() -> URL:
    from src.microservice.core.config import conf

    """Generate a url for db connection."""
    return URL(
        drivername=conf.DATABASE.get("DRIVER", "postgresql"),
        host=conf.DATABASE.get("HOST", "localhost"),
        port=conf.DATABASE.get("PORT", 5432),
        database=conf.DATABASE.get("NAME", "postgres"),
        username=conf.DATABASE.get("USER", "postgres"),
        password=conf.DATABASE.get("PASSWORD", ""),
    )


def get_ssl() -> SSLContext:
    from src.microservice.core.config import conf

    ssl_enable = conf.DATABASE.get("SSL", False)

    if ssl_enable:
        ssl_object = create_default_context(cadata=conf.DATABASE["CA_CERT"])

        return ssl_object


async def init_db():
    bind = get_bind()
    ssl = get_ssl()
    await db.set_bind(
        bind,
        ssl=ssl,
        pool_class=Pool,
        statement_cache_size=0,
    )

    yield db

    await db.pop_bind().close()
