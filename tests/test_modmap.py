import unittest
from unittest import mock
from unittest.mock import call

from .mock_uinput import get_mock_calls, reset_mock
from .helpers import send_keys, get_call_keys, reload_module_assoc_with, debug_log, unittest_verbosity, evt

from xkeysnail.key import Action, Combo, Key, Modifier
from xkeysnail.transform import on_event, define_modmap

class TestModmap(unittest.TestCase):

    def tearDown(self):
        reload_module_assoc_with(on_event);
        reset_mock()

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
            debug_log(keys, expected, get_mock_calls())

        self.assertEqual(get_mock_calls(), expected)

if __name__ == '__main__':
    unittest.main()
