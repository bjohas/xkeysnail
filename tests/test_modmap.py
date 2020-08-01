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

if __name__ == '__main__':
    unittest.main()
