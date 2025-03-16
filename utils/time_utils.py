from datetime import datetime
from typing import Optional, Literal


def get_time_string(timestamp: datetime, delimeter: Literal["_", "-"] = "_"):
    time_string = timestamp.strftime(format="%Y_%m_%d_%H_%M_%S")
    if delimeter != "_":
        time_string = time_string.replace("_", delimeter)

    return time_string
