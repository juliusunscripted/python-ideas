# failing test case with exception

- this test case can be used as an example for
	- structured logging with robot framework and structlog
	- custom listener for full traceback logging

## run test case

### via robotcode (vscode)

- install robotcode extension in vscode
- select testing area in vscode
- press play on test case
- the custom listener gets invoked because it is configured in `robot.toml`


### via cli

- cd into folder `robotframework-tips`

### listeners as path

- run command with default arguments for structlog listener:
	```bash
	robot \
	  --outputdir "output" \
	  --listener "robotframework_tips/utils/robot_listeners/ExceptionTracebackListener.py" \
	  --listener "robotframework_tips/utils/robot_listeners/StructlogListener.py" \
	  "robotframework_tips/examples/failing_test_with_exception/Failing Test.robot"
	```
- run command with custom arguments (colors: bool, full_path: bool) for structlog listener:
	```bash
	robot \
	  --outputdir "output" \
	  --listener "robotframework_tips/utils/robot_listeners/ExceptionTracebackListener.py" \
	  --listener "robotframework_tips/utils/robot_listeners/StructlogListener.py;true;false" \
	  "robotframework_tips/examples/failing_test_with_exception/Failing Test.robot"
	```

### listeners as modules (. dot notion)

- run command with manual arguments for structlog listener:
	```bash
	robot \
	  --console "dotted" \
	  --outputdir "output" \
	  --listener "robotframework_tips.utils.robot_listeners.ExceptionTracebackListener" \
	  --listener "robotframework_tips.utils.robot_listeners.StructlogListener;true;false" \
	  "robotframework_tips/examples/failing_test_with_exception/Failing Test.robot"
	```
