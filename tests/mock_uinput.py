from unittest import mock
with mock.patch('evdev.uinput.UInput') as mock_uinput:
    from xkeysnail.transform import *

# must be imported prior to any xkeysnail.transform imports
# so we have a chance to patch UInput first. 

# also solves problem of trying to do the same in each test
# which proved problematic.

# clear empty call log caused by UInput mock instantiation
mock_uinput.reset_mock()

def get_mock_calls():
    return mock_uinput.mock_calls

def reset_mock():
    mock_uinput.reset_mock()