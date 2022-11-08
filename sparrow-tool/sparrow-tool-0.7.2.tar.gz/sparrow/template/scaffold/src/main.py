from sparrow.log import setup_logging
from sparrow import rel_to_abs
import logging

setup_logging(rel_to_abs("./conf/logging.yaml"))
logger = logging.getLogger("info")
logger.info("hello info.")
logger.warning("hello warning.")
