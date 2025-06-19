# %%
import structlog
import polars as pl
from itables import show
from interactive_window.utils import structlog_utils, jupyter_utils

# %%
structlog_utils.configure_structlog()  # small config log line numbers
jupyter_utils.itables_use_basic_config(
    scrollY="200px"
)  # you can use default height via ()

# %%
log = structlog.stdlib.get_logger()

# %%
log.info("hi :)")

# %%

data = []
for i in range(200):
    data.append({"i": i, "i_squared": i**2})

df = pl.from_dicts(data=data)

# simple print
print(df)

# %%
show(df)

# %%
