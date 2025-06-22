# %%
from robotframework_tips.utils.structlog_utils import configure_structlog
import structlog

# %%

configure_structlog(robotframework_mode=False, full_path=False)

log = structlog.stdlib.get_logger()


# %%
log.info("hi")
# %%
