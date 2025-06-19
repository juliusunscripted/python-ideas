import structlog
from robotframework_tips.utils.structlog_utils import configure_structlog
import logging
import sys

log = structlog.stdlib.get_logger()


class StructlogListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        log.info("initializing structlog...")
        # logging.basicConfig(
        #     format="%(message)s", stream=sys.stderr, level=logging.INFO, force=True
        # )
        configure_structlog()

        log.info("structlog is initialized now")

    # message (structlog as json)
