import unittest, os, sys, time, inspect, pprint
from importlib import reload
from unittest.mock import call

from xkeysnail.key import Action, Combo, Key, Modifier
from evdev import ecodes

pp = pprint.PrettyPrinter(indent=4)

DEFAULT_DEVICE = 'todo'
DEFAULT_DELAY_MS = 50

def send_keys(on_event, keysArr, delayMs=DEFAULT_DELAY_MS):
    """Send array of xkeysnail key events to 'on_event' function

        { k: Key.CAPSLOCK, a: Action.PRESS, device: "some device", s: 50 },
        { k: Key.CAPSLOCK, a: Action.RELEASE, device: "some device", s: 50 },

    - Each key event will be followed by a delayMs sleep or value specified 
      in key 's'
    - If dictionary key 'a' is not specified for a key, will expand to a
      PRESS followed by a RELEASE.
    - Device will be defaulted if key not present.
    """

    # expand shorthand key definitions
    initialLen = len(keysArr)
    for index, key in enumerate(reversed(keysArr)):
        index = (initialLen-index)-1
        # default the 'device' value if not set
        if not 'd' in key:
            key['d'] = DEFAULT_DEVICE
        # if no explicit action, expand to PRESS then RELEASE
        if not 'a' in key and 'k' in key:
            key['a'] = Action.PRESS
            keysArr.insert(index+1, {
                'k': key['k'],
                'a': Action.RELEASE,
                'd': key['d']
            });

    for key in keysArr:
        # allow sleeps between entries by not specifying a key
        if 'k' in key:
            on_event(
                evt(key['k'], key['a']),
                key['d'],
                True
            )

        if 's' in key:
            time.sleep(key['s']/1000)
        else:
            time.sleep(delayMs/1000)

    return keysArr

def transform_to_uinput_calls(keysArr):
    """Generate a mock call list for given key sequence, to be used
       in calls assertions. 
       - Specification of keysArr argument is the same as send_keys.
         (other from having no 'd' or 's' parameters)
    """

    # expand shorthand key definitions
    initialLen = len(keysArr)
    for index, key in enumerate(reversed(keysArr)):
        index = (initialLen-index)-1
        # if no explicit action, expand to PRESS followed by RELEASE
        if not 'a' in key:
            key['a'] = Action.PRESS
            keysArr.insert(index+1, {
                'k': key['k'],
                'a': Action.RELEASE,
            });

    callsArr = []
    for key in keysArr:
        callsArr.append(call().write(ecodes.EV_KEY, key['k'], key['a']))
        callsArr.append(call().syn());

    return callsArr

def reduce_calls(callsArr):
    # remove any redundant writes in callsArr
    # redunant if:
    #  - Key.PRESS when key already pressed
    #  - Key.RELEASE when key already released

    def is_syn(callsEle):
        name, args, kwargs = callsEle
        return name != '().syn'

    # remove syn calls
    callsArr = filter(is_syn, callsArr)

    reduced = []
    pressedKeys = set()
    for callItem in callsArr:
        name, args, kwargs = callItem
        key = args[1]
        action = args[2]
        if action == Action.RELEASE:
            if not key in pressedKeys:
                continue;
            else:
                pressedKeys.remove(key)
        if action == Action.PRESS:
            if key in pressedKeys:
                continue;
            else:
                pressedKeys.add(key)
        reduced.append(callItem)

    # re-interlace syn calls
    callsArr = []
    for callItem in reduced:
        callsArr.append(callItem)
        callsArr.append(call().syn())

    return callsArr

def debug_log(sent, expected, received):
    print('\n# Sent:')
    pp.pprint(sent)
    print('# Received:')
    pp.pprint(received)
    print('# Expected:')
    pp.pprint(expected)

def evt(code, value = Action.PRESS):
    return type('obj', (object,), {
        'code': code,
        'value': value
    })

# to test a complete config
# eval_file(os.path.dirname(os.path.abspath(__file__)) + '/config.py')

# def eval_file(path):
#     with open(path, 'rb') as file:
#         exec(compile(file.read(), path, 'exec'), globals())

def reload_module_assoc_with(fn):
    # :/ reload the module attached to a function
    reload(sys.modules[fn.__module__]);
    # print(1)

def unittest_verbosity():
    """Return the verbosity setting of the currently running unittest
    program, or 0 if none is running.
    """
    #https://stackoverflow.com/a/32883243
    frame = inspect.currentframe()
    while frame:
        self = frame.f_locals.get('self')
        if isinstance(self, unittest.TestProgram):
            return self.verbosity
        frame = frame.f_back
    return 0