import unittest
from unittest import mock
from unittest.mock import call
from importlib import reload

from . import mock_xkeysnail as xkeymock
from . import helpers

from xkeysnail.key import Action, Combo, Key, Modifier
import re

class TestModmap(unittest.TestCase):

    def tearDown(self):
        xkeymock.reset_mock()

    def test_simple_modmap(self):

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

    def test_conditional_modmap(self):

        xkeymock.set_wm_class('test_window_class')

        xkeymock.transform.define_conditional_modmap(re.compile(r'test_window_class'), {
           Key.ENTER: Key.LEFT_CTRL,
        })

        # test with correct wm_class

        keys = xkeymock.send_keys([
            { 'k': Key.ENTER },
        ])

        expected = helpers.transform_to_uinput_calls([
            { 'k': Key.LEFT_CTRL },
        ])

        received = helpers.reduce_calls(xkeymock.get_uinput_calls())

        self.assertEqual(received, expected)

        # test without correct wm_class

        xkeymock.reset_uinput_calls()

        xkeymock.set_wm_class('')

        keys = xkeymock.send_keys([
            { 'k': Key.ENTER },
        ])

        expected = helpers.transform_to_uinput_calls([
            { 'k': Key.ENTER },
        ])

        received = helpers.reduce_calls(xkeymock.get_uinput_calls())

        self.assertEqual(received, expected)

    def test_conditional_modmap_device(self):

        xkeymock.transform.define_conditional_modmap(lambda wm_class, device_name: device_name.startswith('my_device'), {
           Key.ENTER: Key.LEFT_CTRL
        })

        keys = xkeymock.send_keys([
            { 'k': Key.ENTER, 'd': 'my_device' },
        ])

        expected = helpers.transform_to_uinput_calls([
            { 'k': Key.LEFT_CTRL },
        ])

        received = helpers.reduce_calls(xkeymock.get_uinput_calls())

        xkeymock.reset_uinput_calls();

        keys = xkeymock.send_keys([
            { 'k': Key.ENTER, 'd': 'other_device' },
        ])

        expected = helpers.transform_to_uinput_calls([
            { 'k': Key.ENTER },
        ])

        received = helpers.reduce_calls(xkeymock.get_uinput_calls())

        self.assertEqual(received, expected)

if __name__ == '__main__':
    unittest.main()
