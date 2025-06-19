import structlog

log = structlog.stdlib.get_logger()


# https://docs.robotframework.org/docs/extending_robot_framework/custom-libraries/python_library


class TestCase:

    # https://github.com/robotframework/robotframework/blob/master/doc/userguide/src/ExtendingRobotFramework/CreatingTestLibraries.rst
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self._counter = 0

    def count(self):
        self._counter += 1
        print(self._counter)

    def expect_counter(self, expected_value: int):
        if self._counter != expected_value:
            log.error(
                "unexpected value", counter=self._counter, expected_value=expected_value
            )
            raise ValueError("unexpected value for counter")

        log.info(
            "counter value as expected",
            counter=self._counter,
            expected_value=expected_value,
        )
