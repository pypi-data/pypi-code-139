import win32gui
import re

__all__ = ["get_candy_browser_hwnd", "get_51_hwnd"]


def get_candy_browser_hwnd():
    pass


def get_51_hwnd():
    windows_list = list()
    title_list = list()
    hwnd_list = list()

    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), windows_list)
    for window in windows_list:
        title = win32gui.GetWindowText(window)
        pattern = r'\|[0-9]+\|[0-9]+\|[0-9]+'
        if re.search(pattern, title): title_list.append(title)
    for title in title_list:
        hwnd = win32gui.FindWindow(0, title)
        hwnd1 = win32gui.GetDlgItem(hwnd, 0x78)
        hwnd2 = win32gui.GetDlgItem(hwnd1, 0xBE)
        hwnd3 = win32gui.GetDlgItem(hwnd2, 0x1)
        hwnd4 = win32gui.FindWindowEx(hwnd3, None, "MacromediaFlashPlayerActiveX", None)
        hwnd_list.append(hwnd4)

    return hwnd_list
