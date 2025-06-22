import structlog
from robotframework_tips.utils.structlog_utils import configure_structlog

log = structlog.stdlib.get_logger()


class StructlogListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, colors: bool = True, full_path: bool = False):
        log.info("Configuring structlog for Robot Framework...")
        configure_structlog(
            colors=colors, full_path=full_path, robotframework_logger=True
        )

        log.info(
            "structlog is configure now. New logs will be sent to Robot Framework too."
        )
