*** Settings ***
Library     resources/TestCase.py


*** Test Cases ***
Failing test case with exception traceback
    Count
    Count
    # Expecting invalid 3 to force exception
    Expect Counter    expected_value=3
