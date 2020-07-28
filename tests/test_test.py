import unittest, os, sys
from importlib import reload
from unittest import mock
from unittest.mock import MagicMock, call

from evdev import uinput, ecodes
from xkeysnail.key import Action, Combo, Key, Modifier
with mock.patch('evdev.uinput.UInput') as mock_uinput:
    from xkeysnail.transform import on_event, define_modmap

def eval_file(path):
    with open(path, 'rb') as file:
        exec(compile(file.read(), path, 'exec'), globals())

def evt(code, value = Action.PRESS):
    return type('obj', (object,), {
        'code': code,
        'value': value
    })

mock_uinput.syn = MagicMock()
mock_uinput.write_event = MagicMock()
mock_uinput.write = MagicMock()

# clear the empty call()
mock_uinput.reset_mock()

# to test a complete config
# eval_file(os.path.dirname(os.path.abspath(__file__)) + '/config.py')

# todo: support/mock device
# todo: support/mock xlib.display
# todo: helpers for input and expectations
# todo: define unit tests for standard functionality (like this test)
# todo: test for regression test against a complete config
# https://docs.python.org/3/library/unittest.mock-examples.html

def reload_modules():
    # :/ reload transform module
    reload(sys.modules[on_event.__module__]);

class TestTearDown(unittest.TestCase):

    def tearDown(self):
        reload_modules();
        mock_uinput.reset_mock()

    def test_create_modmap(self):

        define_modmap({
            Key.TAB: Key.LEFT_CTRL
        })

        on_event(
            evt(Key.TAB),
            'DEVICE TODO',
            True
        )

        self.assertEqual(mock_uinput.mock_calls, [
            call().write(ecodes.EV_KEY, Key.LEFT_CTRL, Action.PRESS),
            call().syn()
        ])

    def test_previous_modmap_should_no_longer_exist(self):

        # if tearDown is working correctly:
        #   - the modmap defined in first test should no longer exist
        #   - mock_calls should be empty again at start of this test

        on_event(
            evt(Key.TAB),
            'DEVICE TODO',
            True
        )

        self.assertEqual(mock_uinput.mock_calls, [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn()
        ])

if __name__ == '__main__':
    unittest.main()