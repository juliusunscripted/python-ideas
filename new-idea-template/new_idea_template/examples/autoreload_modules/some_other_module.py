import structlog

log = structlog.stdlib.get_logger()


def edit_this_method():
    log.info("edit this log while running interactive window")
