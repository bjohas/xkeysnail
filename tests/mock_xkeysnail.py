from unittest import mock
from importlib import reload
from . import helpers
# patch UInput prior to importing anything from xkeysnail
with mock.patch('evdev.uinput.UInput') as mock_uinput:
    import xkeysnail.output as output
import xkeysnail.transform as transform

# set default window wm_class
transform.get_active_window_wm_class = mock.MagicMock(return_value='')

# clear empty call log caused by UInput mock instantiation
mock_uinput.reset_mock()

def send_keys(keysArr):
    helpers.send_keys(transform.on_event, keysArr)

def set_wm_class(name):
    transform.get_active_window_wm_class = mock.MagicMock(return_value=name)

def reset_mock():
    global mock_uinput
    mock_uinput.reset_mock()
    with mock.patch('evdev.uinput.UInput') as mock_uinput:
        # reload both output and transform modules to reset state
        reload(output)
        reload(transform)
        transform.get_active_window_wm_class = mock.MagicMock(return_value='')
        mock_uinput.reset_mock()

def reset_uinput_calls():
    mock_uinput.reset_mock()

def get_uinput_calls():
    return mock_uinput.mock_calls
