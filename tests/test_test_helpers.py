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

        calls = helpers.get_call_keys([
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

    # enter->left_shift
    # no extra release generated

    # tab->left_ctrl
    # extra release generated

    def test_collapse_extra_release_removes(self):

        result = helpers.collapse_extra_release([
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

    def test_collapse_extra_release_syn_sensitive(self):

        expected = [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().syn(),
        ]

        # should be a nop
        result = helpers.collapse_extra_release(expected);

        self.assertEqual(result, expected)


    def test_collapse_extra_release_matches_key(self):

        expected = [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.LEFT_CTRL, Action.RELEASE),
            call().syn(),
        ]

        # should be a nop
        result = helpers.collapse_extra_release(expected)

        self.assertEqual(result, expected)

    def test_collapse_extra_release_respects_bounds(self):

        expected = [
            call().write(ecodes.EV_KEY, Key.TAB, Action.PRESS),
            call().syn(),
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE),
        ]

        # should be a nop
        result = helpers.collapse_extra_release(expected)

        self.assertEqual(result, expected)

        expected = [
            call().write(ecodes.EV_KEY, Key.TAB, Action.RELEASE)
        ]

        # should be a nop
        result = helpers.collapse_extra_release(expected)

        self.assertEqual(result, expected)