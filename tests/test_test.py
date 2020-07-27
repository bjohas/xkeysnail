import unittest
import os
from unittest import mock
from unittest.mock import MagicMock, call
from xkeysnail.key import Action, Combo, Key, Modifier
from evdev import uinput
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

mock_uinput.syn = MagicMock();
mock_uinput.write_event = MagicMock();
mock_uinput.write = MagicMock();

# to test a complete config
# eval_file(os.path.dirname(os.path.abspath(__file__)) + '/config.py')

class TestSetup(unittest.TestCase):

    def test_test(self):

        mock_uinput.reset_mock()

        # todo: support/mock device
        # todo: support/mock xlib.display
        # todo: helpers for input and expectations
        # https://docs.python.org/3/library/unittest.mock-examples.html

        define_modmap({
            Key.CAPSLOCK: Key.LEFT_CTRL
        })

        on_event(
            evt(Key.CAPSLOCK),
            'DEVICE TODO',
            True
        )

        self.assertEqual(mock_uinput.mock_calls, [
            call().write(1, Key.LEFT_CTRL, Action.PRESS),
            call().syn()
        ])
#       print(mock_uinput.mock_calls)

if __name__ == '__main__':
    unittest.main()