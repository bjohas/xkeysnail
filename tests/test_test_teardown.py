import unittest
from unittest import mock
from unittest.mock import call
from evdev import uinput, ecodes

from . import mock_uinput as uinput
from . import helpers

from xkeysnail.key import Action, Combo, Key, Modifier
from xkeysnail.transform import on_event, define_modmap

class TestTearDown(unittest.TestCase):

    # testing that we're not retaining state between tests

    # if tearDown is working correctly:
    #   - the modmap defined in first test should no longer exist
    #   - mock_calls should be empty again at start of this test

    def tearDown(self):
        # force reload of xkeysnail
        helpers.reload_module_assoc_with(on_event);
        uinput.reset_mock()

    def test_simple_modmap(self):

        define_modmap({
            Key.TAB: Key.LEFT_CTRL
        })

        keys = helpers.send_keys(on_event, [
            { 'k': Key.TAB },
            { 'k': Key.TAB },
        ])

        expected = helpers.get_call_keys([
            { 'k': Key.LEFT_CTRL },
            { 'k': Key.LEFT_CTRL }
        ])

        received = helpers.collapse_extra_release(uinput.get_mock_calls())

        self.assertEqual(received, expected)

    def test_simple_modmap_should_no_longer_exist(self):

        # this is also example of interacting without use of the helpers

        on_event(
            helpers.evt(Key.TAB),
            'DEVICE TODO',
            True
        )

        received = helpers.collapse_extra_release(uinput.get_mock_calls())

        self.assertEqual(received, [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn()
        ])

if __name__ == '__main__':
    unittest.main()
