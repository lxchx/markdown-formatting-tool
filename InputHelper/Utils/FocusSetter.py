from ctypes import windll, wintypes

GWL_STYLE = -16
GWL_EXSTYLE = -20
WS_CHILD = 0x40000000
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000

SWP_FRAMECHANGED = 0x0020
SWP_NOACTIVATE = 0x0010
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001

GetWindowLong = windll.user32.GetWindowLongW
GetWindowLong.restype = wintypes.ULONG
GetWindowLong.argtpes = (wintypes.HWND, wintypes.INT)
SetWindowLong = windll.user32.SetWindowLongW
SetWindowLong.restype = wintypes.ULONG
SetWindowLong.argtpes = (wintypes.HWND, wintypes.INT, wintypes.ULONG)
SetWindowPos = windll.user32.SetWindowPos

def set_no_focus(hwnd):
    style = GetWindowLong(hwnd, GWL_EXSTYLE) # get existing style
    style = style & ~WS_EX_TOOLWINDOW # remove toolwindow style
    style = style | WS_EX_NOACTIVATE | WS_EX_APPWINDOW
    res = SetWindowLong(hwnd, GWL_EXSTYLE, style)
    res = SetWindowPos(hwnd, 0, 0,0,0,0, SWP_FRAMECHANGED | SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE)