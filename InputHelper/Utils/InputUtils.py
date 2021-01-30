import string
import ctypes
import ctypes.wintypes

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

VK_SHIFT = 0x10  # Shift key
# special keys
VK_OEM_1 = 0xBA
VK_OEM_PLUS = 0xBB
VK_OEM_COMMA = 0xBC
VK_OEM_MINUS = 0xBD
VK_OEM_PERIOD = 0xBE
VK_OEM_2 = 0xBF
VK_OEM_3 = 0xC0
VK_OEM_4 = 0xDB
VK_OEM_5 = 0xDC
VK_OEM_6 = 0xDD
VK_OEM_7 = 0xDE
KEYEVENTF_KEYUP = 0x0002  # Releases the key
INPUT_KEYBOARD = 1

UPPER = frozenset('~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?')
LOWER = frozenset("`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./")
ORDER = string.ascii_letters + string.digits + ' \b\r\t'
ALTER = dict(zip('!@#$%^&*()', '1234567890'))
OTHER = {
    '`': VK_OEM_3,
    '~': VK_OEM_3,
    '-': VK_OEM_MINUS,
    '_': VK_OEM_MINUS,
    '=': VK_OEM_PLUS,
    '+': VK_OEM_PLUS,
    '[': VK_OEM_4,
    '{': VK_OEM_4,
    ']': VK_OEM_6,
    '}': VK_OEM_6,
    '\\': VK_OEM_5,
    '|': VK_OEM_5,
    ';': VK_OEM_1,
    ':': VK_OEM_1,
    "'": VK_OEM_7,
    '"': VK_OEM_7,
    ',': VK_OEM_COMMA,
    '<': VK_OEM_COMMA,
    '.': VK_OEM_PERIOD,
    '>': VK_OEM_PERIOD,
    '/': VK_OEM_2,
    '?': VK_OEM_2
}


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD), ('wScan', WORD), ('dwFlags', DWORD),
                ('time', DWORD), ('dwExtraInfo', ULONG_PTR))


class INPUT(ctypes.Structure):
    _fields_ = ('type', DWORD), ('ki', KEYBDINPUT), ('pad', ctypes.c_ubyte * 8)


def Input(structure):
    return INPUT(INPUT_KEYBOARD, structure)


def KeyboardInput(code, flags):
    return KEYBDINPUT(code, code, flags, 0, None)


def Keyboard(code, flags=0):
    return Input(KeyboardInput(code, flags))


def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)


def stream(string):
    mode = False
    for character in string.replace('\r\n', '\r').replace('\n', '\r'):
        if mode and character in LOWER or not mode and character in UPPER:
            yield Keyboard(VK_SHIFT, mode and KEYEVENTF_KEYUP)
            mode = not mode
        character = ALTER.get(character, character)
        if character in ORDER:
            code = ord(character.upper())
        elif character in OTHER:
            code = OTHER[character]
        else:
            # continue
            raise ValueError('Undecoded')
        yield Keyboard(code)
        yield Keyboard(code, KEYEVENTF_KEYUP)
    if mode:
        yield Keyboard(VK_SHIFT, KEYEVENTF_KEYUP)

#only support char in keyboard
def send_keys(text: str):
    for k in stream(text):
        SendInput(k)


if __name__ == '__main__':
    import time

    def demo(wait=3):
        time.sleep(wait)
        send_keys("nice")

    demo()