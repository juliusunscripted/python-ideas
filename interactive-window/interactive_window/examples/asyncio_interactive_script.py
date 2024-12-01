# %% [markdown]
# # Use same asyncio code for interactive window and script
#
# - ipykernel runs an asyncio event loop automatically ([more info in blog post: IPython 7.0, Async REPL](https://blog.jupyter.org/ipython-7-0-async-repl-a35ce050f7f7))
# - so we can use async await code without having to think about the event loop
# - but ususally async await code can only be exectued in async def/async content
# - that is why vscode/pylance show errors in case there is an await coroutine statement in an interactive windows code file
# - the code runs perfectly fine when executed in an interactive windows
# - but of course the error is annoying
# - furthermore you are not able to just run the whole python file
#
# ## Goal of this example
#
# - use async await code in interactive window python file
# - provide a general structure for developing asyncio code in interactive window
# - while still being able to run the whole python file as a *normal* script
#
# ## How to run this code?
#
# - you can press on *Run Above* of the last cell at the bottom to run the whole script in interactive window mode in vscode
# - you can press the play button at the top right to run the whole script as a *normal* python script
# - you can the the script via the following command:
#   ```bash
#   python -m interactive_window.examples.example_01_asyncio
#   ```

# %%
import asyncio
import structlog
from interactive_window.utils import structlog_utils

# %%
structlog_utils.configure_structlog()  # small config log line numbers

# %%
log = structlog.stdlib.get_logger()

# %%
log.info("hi :)")

# the following command...
# await asyncio.sleep(1)
# would result in an pylance error: "await" allowed only within async function

# %%


# the main argument `interactive_window_mode` is not required
# but perhaps you want to use it as condition in your code
async def main(interactive_window_mode: bool = True):
    # this clever cell trick is important!
    # keep the 'pass' statement so the interactive window cell is valid code

    pass
    # start a new cell now with `# %%`

    # %%
    # ensure that variable `interactive_window_mode` is available while running in interactive window mode
    # the variable is not required but perhaps you want to use it as condition in your code
    if "interactive_window_mode" not in locals():
        interactive_window_mode = True

    # %%
    log.info(
        "i am running in this mode", interactive_window_mode=interactive_window_mode
    )

    # %%
    # continue with your code which can be executed exactly the same in interactive window...
    # ... but even as a normal python file because `async main()` will be executed then (see `if __main__` code at the bottom)
    #
    # %%

    # this code is not indented in interactive window so you can just run it like usual (e. g. shift + enter)
    all_values_added = 0

    log.info("doing some async code...")
    for i in range(5):
        log.info("hi", i=i)
        all_values_added += i
        await asyncio.sleep(0.5)
    log.info("that's it")

    # %%

    log.info("added all values", all_values_added=all_values_added)

    # %%

    if not interactive_window_mode:
        # code cells below will not be executed by script run
        exit()

    # %%
    print(
        (
            "some more code that will not be executed when running the python script\n"
            "but it will be executed in interactive window mode"
        )
    )


# %%
if __name__ == "__main__":
    try:
        asyncio.get_running_loop()
        # will happen when executed in interactive window
        detected_interactive_window_mode = True
    except RuntimeError:
        # will happen if executed as normal python file
        detected_interactive_window_mode = False

    log.info(
        "detection of mode",
        detected_interactive_window_mode=detected_interactive_window_mode,
    )

    if not detected_interactive_window_mode:
        log.info("will run async main now")
        # the main argument `interactive_window_mode` is not required
        # but perhaps you want to use it as condition in your code
        asyncio.run(main(interactive_window_mode=detected_interactive_window_mode))
    else:
        log.warning(
            (
                "this code cell is only needed when running the file as normal python script\n"
                "It will not do anything when being executed in interactive window"
            ),
            detected_interactive_window_mode=detected_interactive_window_mode,
        )


# %% [markdown]

# - you can press on *Run Above* of this cell to run the whole script in interactive window mode in vscode
# - you can press the play button at the top right to run the whole script as a *normal* python script
# - you can the the script via the following command:
#   ```bash
#   python -m interactive_window.examples.example_01_asyncio
#   ```
