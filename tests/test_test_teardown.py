import unittest
from unittest import mock
from unittest.mock import MagicMock, call

from evdev import uinput, ecodes
from xkeysnail.key import Action, Combo, Key, Modifier
with mock.patch('evdev.uinput.UInput') as mock_uinput:
    from xkeysnail.transform import on_event, define_modmap

from .helpers import send_keys, get_call_keys, reload_modules, debug_log, unittest_verbosity, evt

mock_uinput.syn = MagicMock()
mock_uinput.write_event = MagicMock()
mock_uinput.write = MagicMock()

# clear the empty call()
mock_uinput.reset_mock()

class TestTearDown(unittest.TestCase):

    # testing that we're not retaining state between tests

    # if tearDown is working correctly:
    #   - the modmap defined in first test should no longer exist
    #   - mock_calls should be empty again at start of this test

    def tearDown(self):
        reload_modules(on_event);
        mock_uinput.reset_mock()

    def test_simple_modmap(self):

        define_modmap({
            Key.TAB: Key.LEFT_CTRL
        })

        keys = send_keys(on_event, [
            { 'k': Key.TAB },
            { 'k': Key.TAB },
        ])

        expected = get_call_keys([
            { 'k': Key.LEFT_CTRL },
            { 'k': Key.LEFT_CTRL }
        ])

        if unittest_verbosity() >= 2:
            debug_log(keys, expected, mock_uinput.mock_calls)

        self.assertEqual(mock_uinput.mock_calls, expected)

    def test_simple_modmap_should_no_longer_exist(self):

        # this is also example of interacting without use of the helpers

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
