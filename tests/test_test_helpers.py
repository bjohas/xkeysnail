import unittest
from unittest import mock
from unittest.mock import call
from evdev import ecodes

from . import helpers

from xkeysnail.key import Action, Combo, Key, Modifier

class TestHelpers(unittest.TestCase):

    # some tests for the main helper functions

    def test_send_key_action_expansion(self):

        def dummy(x, y, z):
            return

        keys = helpers.send_keys(dummy, [
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

        calls = helpers.transform_to_uinput_calls([
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

    def test_collapse_extra_release_removes(self):

        result = helpers.reduce_calls([
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().syn(),
        ])

        expected = [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().syn()
        ]

        self.assertEqual(result, expected)

    def test_reduce_multiple_redundant_calls(self):

        callsArr = [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.LEFT_SHIFT, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().syn(),
        ];

        result = helpers.reduce_calls(callsArr)

        expected = [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.LEFT_SHIFT, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().syn(),
        ]

        self.assertEqual(result, expected)
