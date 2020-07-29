import unittest
from unittest import mock
from unittest.mock import call
from evdev import ecodes

from .helpers import send_keys, get_call_keys, evt

from xkeysnail.key import Action, Combo, Key, Modifier

class TestHelpers(unittest.TestCase):

    # some tests for the main helper functions

    def test_send_key_action_expansion(self):

        def dummy(x, y, z):
            return

        keys = send_keys(dummy, [
            { 'k': Key.TAB, 'd': '' },
            { 'k': Key.ENTER, 'd': '' },
        ])

        expected = [
            { 'k': Key.TAB, 'd': '', 'a': Action.PRESS },
            { 'k': Key.TAB, 'd': '', 'a': Action.RELEASE },
            { 'k': Key.ENTER, 'd': '', 'a': Action.PRESS },
            { 'k': Key.ENTER, 'd': '', 'a': Action.RELEASE }
        ]

        self.assertEqual(keys, expected)

    def test_call_key_action_expansion(self):

        calls = get_call_keys([
            { 'k': Key.TAB },
            { 'k': Key.ENTER },
        ])

        expected = [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.ENTER, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.ENTER, Action.RELEASE),
            call().syn(),
        ]

        self.assertEqual(calls, expected)

    def test_call_key_modifier_release_double(self):

        calls = get_call_keys([
            { 'k': Key.LEFT_SHIFT, 'a': Action.PRESS },
            { 'k': Key.LEFT_SHIFT, 'a': Action.RELEASE },
            { 'k': Key.LEFT_SHIFT },
        ])

        expected = [
            call().write(ecodes.EV_KEY, Key.LEFT_SHIFT, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.LEFT_SHIFT, Action.RELEASE),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.LEFT_SHIFT, Action.RELEASE),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.LEFT_SHIFT, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.LEFT_SHIFT, Action.RELEASE),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.LEFT_SHIFT, Action.RELEASE),
            call().syn()
        ]

        self.assertEqual(calls, expected)

        calls = get_call_keys([
            { 'k': Key.LEFT_SHIFT },
            { 'k': Key.LEFT_SHIFT }
        ])

        self.assertEqual(calls, expected)