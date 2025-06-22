# https://github.com/hynek/structlog/issues/546#issuecomment-1741258252
import logging
import structlog
from pprint import pprint

import sys
import json

from structlog.typing import EventDict, WrappedLogger


class RobotLog:

    def __init__(self):

        try:
            # only import robotframework dependencies in case robot logger gets used
            from robot.api import logger

            self.robot_logger = logger
        except:
            print("you must install robotframework to use this feature")
            raise

    def __call__(
        self, logger: WrappedLogger, name: str, event_dict: EventDict
    ) -> EventDict:

        copied_event_dict = dict(event_dict)
        level = copied_event_dict.pop("level", None)
        event = copied_event_dict.pop("event", None)

        logger_func = self.robot_logger.debug

        match level:
            case "debug":
                logger_func = self.robot_logger.debug
            case "info":
                logger_func = self.robot_logger.info
            case "warning":
                logger_func = self.robot_logger.warn
            case "error":
                logger_func = self.robot_logger.error
            case _:
                print("unexpected log level", level)
                logger_func = self.robot_logger.debug

        msg = f"{event}"
        if copied_event_dict:
            msg += f" | {json.dumps(copied_event_dict, ensure_ascii=False)}"
        logger_func(msg=msg, html=False)

        return event_dict


class LogJump:
    def __init__(
        self,
        full_path: bool = False,
    ) -> None:
        self.full_path = full_path

    def __call__(
        self, logger: WrappedLogger, name: str, event_dict: EventDict
    ) -> EventDict:
        if self.full_path:
            file_part = event_dict.pop("pathname")
        else:
            file_part = event_dict.pop("filename")

        # leading space improves link recognition in vscode (but spaces in paths still do not work always)
        event_dict["_l"] = f' {file_part}:{event_dict.pop("lineno")}'

        return event_dict


def configure_structlog(
    colors: bool = True, full_path: bool = False, robotframework_logger: bool = False
):
    """configure structlog with useful defaults and additional features

    Args:
        colors (bool, optional): create colorful logs. Defaults to True.
        full_path (bool, optional): location entry contains full path instead of only file name. Defaults to False.
        robotframework_logger (bool, optional): send logs to robotframework log output (requires robotframework to be installed and used). Defaults to False.
    """

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
    ]
    if robotframework_logger:
        processors.append(RobotLog())

    call_site_parameters = [structlog.processors.CallsiteParameter.LINENO]
    # add either pathname or filename and then set full_path to True or False in LogJump below
    if full_path:
        call_site_parameters.append(structlog.processors.CallsiteParameter.PATHNAME)
    else:
        call_site_parameters.append(structlog.processors.CallsiteParameter.FILENAME)

    processors.extend(
        [
            structlog.processors.CallsiteParameterAdder(call_site_parameters),
            LogJump(full_path=full_path),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.dev.ConsoleRenderer(colors=colors),
        ]
    )

    if robotframework_logger:
        # use stderr in case of robot framework so logs do not get captured twice
        logger_factory = structlog.PrintLoggerFactory(file=sys.stderr)
    else:
        # use stdout (default in case structlog gets use without robot framework)
        logger_factory = structlog.PrintLoggerFactory()
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=logger_factory,
        cache_logger_on_first_use=False,
    )


if __name__ == "__main__":

    configure_structlog()
    log = structlog.stdlib.get_logger()

    log.info("Hi!", asdf="asdf", fdsa=123456789, abcdefghijklmnopq="987654321")
