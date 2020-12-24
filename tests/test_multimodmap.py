import unittest
from unittest import mock
from unittest.mock import call
from importlib import reload

from . import mock_xkeysnail as xkey_mock
from . import helpers

from xkeysnail.key import Action, Combo, Key, Modifier

class TestMultiModmap(unittest.TestCase):

    def tearDown(self):
        xkey_mock.reset_mock()

    def test_multipurpose_modmap(self):

        xkey_mock.transform.define_multipurpose_modmap({
            Key.LEFT_CTRL: [Key.KPLEFTPAREN, Key.LEFT_SHIFT],
        })

        keys = xkey_mock.send_keys([
            { 'k': Key.LEFT_CTRL },
        ])

        expected = helpers.transform_to_uinput_calls([
            { 'k': Key.KPLEFTPAREN },
        ])

        received = helpers.reduce_calls(xkey_mock.get_uinput_calls())

        self.assertEqual(received, expected)

        xkey_mock.reset_uinput_calls()

        # We have to send a key following the modifier, as 
        # xkeysnail only sends modifier for multipurpose maps
        # on subsequent key-presses

        keys = xkey_mock.send_keys([
            { 'k': Key.LEFT_CTRL, 'a': Action.PRESS },
            { 's': 100 },
            { 'k': Key.A },
        ])

        expected = helpers.transform_to_uinput_calls([
            { 'k': Key.LEFT_SHIFT, 'a': Action.PRESS },
            { 'k': Key.A },
        ])

        received = helpers.reduce_calls(xkey_mock.get_uinput_calls())

        self.assertEqual(received, expected)

    ### Ideally, xkeysnail would pass this test:
    #
    # def test_multipurpose_modmap_with_timer(self):
    #
    #     xkey_mock.transform.define_multipurpose_modmap({
    #         Key.LEFT_CTRL: [Key.KPLEFTPAREN, Key.LEFT_SHIFT],
    #     })
    #
    #     keys = xkey_mock.send_keys([
    #         { 'k': Key.LEFT_CTRL },
    #     ])
    #
    #     expected = helpers.transform_to_uinput_calls([
    #         { 'k': Key.KPLEFTPAREN },
    #     ])
    #
    #     received = helpers.reduce_calls(xkey_mock.get_uinput_calls())
    #
    #     self.assertEqual(received, expected)
    #
    #     xkey_mock.reset_uinput_calls()
    #
    #     keys = xkey_mock.send_keys([
    #         { 'k': Key.LEFT_CTRL, 'a': Action.PRESS },
    #         { 's': 100 },
    #     ])
    #
    #     expected = helpers.transform_to_uinput_calls([
    #         { 'k': Key.LEFT_SHIFT, 'a': Action.PRESS },
    #     ])
    #
    #     received = helpers.reduce_calls(xkey_mock.get_uinput_calls())
    #
    #     self.assertEqual(received, expected)


if __name__ == '__main__':
    unittest.main()
