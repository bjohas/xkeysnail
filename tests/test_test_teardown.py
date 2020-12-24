import unittest
from unittest import mock
from unittest.mock import call
from evdev import ecodes
from importlib import reload

from . import mock_xkeysnail as xkeymock
from . import helpers

from xkeysnail.key import Action, Combo, Key, Modifier

class TestTearDown(unittest.TestCase):

    # testing that we're not retaining state between tests

    # if tearDown is working correctly:
    #   - the modmap defined in first test should no longer exist
    #   - mock_calls should be empty again at start of this test

    def tearDown(self):
        xkeymock.reset_mock()

    def test_create_modmap(self):

        xkeymock.transform.define_modmap({
            Key.TAB: Key.LEFT_CTRL
        })

        keys = xkeymock.send_keys([
            { 'k': Key.TAB },
            { 'k': Key.TAB },
        ])

        expected = helpers.transform_to_uinput_calls([
            { 'k': Key.LEFT_CTRL },
            { 'k': Key.LEFT_CTRL }
        ])

        received = helpers.reduce_calls(xkeymock.get_uinput_calls())

        self.assertEqual(received, expected)

    def test_simple_modmap_should_no_longer_exist(self):
        # this tests that state is not retained in xkeysnail.transform
        # following tearDown

        # this is also example of interacting without use of the helpers

        xkeymock.transform.on_event(
            helpers.evt(Key.TAB),
            'DEVICE TODO',
            True
        )

        received = helpers.reduce_calls(xkeymock.get_uinput_calls())

        self.assertEqual(received, [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn()
        ])

    def test_uinput_calls_can_be_reset(self):

        xkeymock.transform.define_modmap({
            Key.TAB: Key.LEFT_CTRL
        })

        keys = xkeymock.send_keys([
            { 'k': Key.TAB },
            { 'k': Key.TAB },
        ])

        self.assertNotEqual(xkeymock.get_uinput_calls(), [])

        xkeymock.reset_uinput_calls()

        self.assertEqual(xkeymock.get_uinput_calls(), [])

if __name__ == '__main__':
    unittest.main()
