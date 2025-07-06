# https://github.com/hynek/structlog/issues/546#issuecomment-1741258252
import logging
import structlog

from structlog.typing import EventDict, WrappedLogger


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
            file_part = "\n" + event_dict.pop("pathname")
        else:
            file_part = event_dict.pop("filename")
        event_dict["_l"] = f'"{file_part}:{event_dict.pop("lineno")}"'

        return event_dict


def configure_structlog():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.processors.CallsiteParameterAdder(
                [
                    # add either pathname or filename and then set full_path to True or False in LogJump below
                    # structlog.processors.CallsiteParameter.PATHNAME,
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ],
            ),
            LogJump(full_path=False),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )


if __name__ == "__main__":

    configure_structlog()
    log = structlog.stdlib.get_logger()

    log.info("Hi!", asdf="asdf", fdsa=123456789, abcdefghijklmnopq="987654321")
