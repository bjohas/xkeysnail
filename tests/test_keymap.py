import unittest
from unittest import mock
from unittest.mock import call
from importlib import reload

from . import mock_xkeysnail as xkeymock
from . import helpers

from xkeysnail.key import Action, Combo, Key, Modifier
import re

class TestKeymap(unittest.TestCase):

    def tearDown(self):
        xkeymock.reset_mock()

    def test_keymap(self):

        K = xkeymock.transform.K

        xkeymock.transform.define_modmap({
           Key.CAPSLOCK: Key.LEFT_CTRL,
        })

        xkeymock.transform.define_keymap(None, {
            K("C-c"): K("LAlt-Enter"),
        })

        # test with correct wm_class

        keys = xkeymock.send_keys([
            { 'k': Key.CAPSLOCK, 'a': Action.PRESS },
            { 'k': Key.C, 'a': Action.PRESS },
            { 'k': Key.C, 'a': Action.RELEASE }
        ])

        expected = helpers.transform_to_uinput_calls([
            { 'k': Key.LEFT_CTRL, 'a': Action.PRESS },
            { 'k': Key.LEFT_CTRL, 'a': Action.RELEASE },
            { 'k': Key.LEFT_ALT, 'a': Action.PRESS },
            { 'k': Key.ENTER, 'a': Action.PRESS },
            { 'k': Key.ENTER, 'a': Action.RELEASE },
            { 'k': Key.LEFT_CTRL, 'a': Action.PRESS }
            # should there not be a 'left_alt' release also?
        ])

        received = helpers.reduce_calls(xkeymock.get_uinput_calls())

        # print(received)

        self.assertEqual(received, expected)

if __name__ == '__main__':
    unittest.main()
