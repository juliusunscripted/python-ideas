# %% [markdown]
# # Avoid having to reimport changed modules
#
# - while development you change code in different modules outside of the interactive window script
# - usually you would have to restart the kernel or at least run the cells with the import commands again
# - otherwise changed code would not be available in the running kernel
#
# ## Solution: autoreload
#
# - there is a jupyter/ipython feature called [autoreload](https://ipython.org/ipython-doc/3/config/extensions/autoreload.html)
# - you have to adjust this setting in vscode to be able to use it
#   ```json
#   {
#     "jupyter.interactiveWindow.textEditor.magicCommandsAsComments": true,
#   }
#
# ## Follow example below
#
# Now you can configure autoreload for specific module file as shown below


# %%
# !%load_ext autoreload
# !%autoreload 1

# !%aimport interactive_window.examples.autoreload_modules.some_other_module


# %%
import structlog
import polars as pl
from itables import show
from interactive_window.utils import structlog_utils
from interactive_window.examples.autoreload_modules import some_other_module

# %%
structlog_utils.configure_structlog()  # small config log line numbers

# %%
log = structlog.stdlib.get_logger()

# %%
log.info("hi :)")

# %%

# run this first with the original code
some_other_module.edit_this_method()

# %% [markdown]

# - now change the log line text inside `edit_this_method()` and save the file
# - then run the cell below
# - it should show the changed text

# %%

some_other_module.edit_this_method()

# %% [markdown]

# # What is cool about this?
#
# You did not have to restart the kernel or reimport the module manually
# %%
