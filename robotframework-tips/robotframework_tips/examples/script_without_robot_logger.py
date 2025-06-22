# %%
from robotframework_tips.utils.structlog_utils import configure_structlog
import structlog

# %%


# this will work even if robotframework is not installed
# (but fail with explanation in case robotframework_mode gets set to True and robotframework is not installed)
configure_structlog(robotframework_mode=False, full_path=False)

# %%

log = structlog.stdlib.get_logger()


# %%
log.info("hi")
# %%
