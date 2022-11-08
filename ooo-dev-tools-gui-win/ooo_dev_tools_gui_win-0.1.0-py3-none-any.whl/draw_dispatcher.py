from __future__ import annotations

import uno
from com.sun.star.drawing import XShape
from com.sun.star.drawing import XDrawPage

from ooodev.utils.lo import Lo
from ooodev.office.draw import Draw

import pywinauto
from pywinauto.application import Application


class DrawDispatcher:
    """Draw Dispat Automation"""

    @staticmethod
    def create_dispatch_shape_win(slide: XDrawPage, shape_dispatch: str) -> XShape | None:
        """
        Creates a dispatch shape in two steps.

        1. Select the shape by calling ``Lo.dispatch_cmd()``
        2. Creates the shape on screen by imitating a press and drag on the visible page.

        A reference to the created shape is obtained by assuming that it's the new
        top-most element on the page.

        Args:
            slide (XDrawPage): Draw Page
            shape_dispatch (str): Shape Dispatch Command

        Returns:
            XShape | None: Shape on Success; Otherwise, ``None``.
        """
        num_shapes = slide.getCount()

        # select the shape icon; Office must be visible
        Lo.dispatch_cmd(shape_dispatch)
        # wait just a sec.
        Lo.delay(1_000)

        # click and drag on the page to create the shape on the page;
        # the current page must be visible
        app = Application().connect(title_re=".*LibreOffice Draw", class_name="SALFRAME")

        win = app.window(title_re=".*LibreOffice Draw")
        win.set_focus()
        Lo.delay(500)
        rect = win.rectangle()
        center_x = round((rect.right - rect.left) / 2) + rect.left
        center_y = round((rect.bottom - rect.top) / 2) + rect.top

        pywinauto.mouse.press(button="left", coords=(center_x, center_y))
        pywinauto.mouse.release(button="left", coords=(center_x + 50, center_y + 50))

        # get a reference to the shape by assuming it's the top one on the page
        num_shapes2 = slide.getCount()
        if num_shapes2 == num_shapes + 1:
            Lo.print(f'Shape "{shape_dispatch}" created')
            return Draw.find_top_shape(slide)
        else:
            Lo.print(f'Shape "{shape_dispatch}" NOT created')
            return None
