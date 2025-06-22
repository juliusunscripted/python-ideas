from robot.libraries.BuiltIn import BuiltIn
from robot import running, result
from robot.api import logger as robot_logger
from robot.utils.error import get_error_details


class ExceptionTracebackListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    # https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-version-3
    def end_keyword(self, data: running.Keyword, result: result.Keyword):
        elapsed_seconds = result.elapsed_time.total_seconds()
        if result.status == "FAIL":

            error_message, error_traceback = get_error_details(full_traceback=True)

            error_log = (
                f"keyword failed with error message: {error_message}\n"
                f"{error_traceback}"
            )
            robot_logger.error(msg=error_log)
