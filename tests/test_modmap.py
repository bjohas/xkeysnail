import unittest
from unittest import mock
from unittest.mock import call

from . import mock_uinput as uinput
from . import helpers

from xkeysnail.key import Action, Combo, Key, Modifier
from xkeysnail.transform import on_event, define_modmap, define_conditional_modmap

import re

class TestModmap(unittest.TestCase):

    def tearDown(self):
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

    @mock.patch('xkeysnail.transform.get_active_window_wm_class')
    def test_conditional_modmap(self, get_wm_class):

        define_conditional_modmap(re.compile(r'test_window_class'), {
           Key.ENTER: Key.LEFT_CTRL,
        })

        # test with correct wm_class

        get_wm_class.return_value = 'test_window_class'

        keys = helpers.send_keys(on_event, [
            { 'k': Key.ENTER },
        ])

        expected = helpers.get_call_keys([
            { 'k': Key.LEFT_CTRL },
        ])

        received = helpers.collapse_extra_release(uinput.get_mock_calls())

        self.assertEqual(received, expected)

        # test without correct wm_class

        uinput.reset_mock()
        get_wm_class.return_value = ''

        keys = helpers.send_keys(on_event, [
            { 'k': Key.ENTER },
        ])

        expected = helpers.get_call_keys([
            { 'k': Key.ENTER },
        ])

        received = helpers.collapse_extra_release(uinput.get_mock_calls())

        self.assertEqual(received, expected)

if __name__ == '__main__':
    unittest.main()
