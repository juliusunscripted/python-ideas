from robot import running, result
from robot.api import logger as robot_logger
from robot.utils.error import get_error_details
from typing import Literal


class ExceptionTracebackListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(
        self,
        exception_details_log_level: Literal["DEBUG", "INFO", "WARN", "ERROR"] = "INFO",
    ):
        match exception_details_log_level:
            case "DEBUG":
                self.logger_func = robot_logger.debug
            case "INFO":
                self.logger_func = robot_logger.info
            case "WARN":
                self.logger_func = robot_logger.warn
            case "ERROR":
                self.logger_func = robot_logger.error
            case _:
                raise ValueError("invalid value for exception_details_log_level")

    # https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-version-3
    def end_keyword(self, data: running.Keyword, result: result.Keyword):
        if result.status == "FAIL":
            error_message, error_traceback = get_error_details(full_traceback=True)

            trace_details = (
                f"keyword failed with error message: {error_message}\n"
                f"{error_traceback}"
            )
            self.logger_func(msg=trace_details)
