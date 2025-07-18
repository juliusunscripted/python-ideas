# interactive window

> in case you need help for getting started: follow instructions of repo [new-python-project](https://github.com/suiluj/new-python-project)

- this section show some ideas, tips and tricks for working with python interactive window in vscode


## Important setup steps

- install recommended extension:
	- python
	- jupyter
- add the following useful settings in your vscode `settings.json`
	```json
	{
		"jupyter.interactiveWindow.textEditor.executeSelection": true,
		"jupyter.interactiveWindow.textEditor.magicCommandsAsComments": true,
		"interactiveWindow.collapseCellInputCode": "never",
		"interactiveWindow.executeWithShiftEnter": true,
		"git.openRepositoryInParentFolders": "always"
	}
	```


## Interesting links

- [Python Interactive window](https://code.visualstudio.com/docs/python/jupyter-support-py)


## Examples

- [asyncio_interactive_script](interactive_window/examples/asyncio_interactive_script.py)
	- use the same asyncio code for python scripts and interactive window
- [autoreload_modules](interactive_window/examples/autoreload_modules/autoreload_modules.py)
	- how to use autoreload in interactvie window with special setting `magicCommandsAsComments`
- [interactive_table](interactive_window/examples/interactive_table.py)
	- use `itables` with easy to use default settings to show dataframe in an interactive way
- example_03_interactive_async_playwright (planned)
	- use playwright async api (which can be used in jupyter notebooks/interactive window ipykernel)
	- showing some examples
- example_04_playwright_chrome_debug_session
	- use your usual chrome browswer for web automation
	- this can have some advantages and disadvantage (usefulness depends on you usecase)
