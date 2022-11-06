import os, time, json
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog

from py_simple_ttk import (
    ScrolledCanvas,
    LabeledEntry,
    check_in_bounds,
    get_friendly_time,
    get_asset,
)

from .BubbleLib import NoteEntry

BUBBLE_SIDE_SPACING = 20
SCROLLBAR_WIDTH = 15
BUBBLE_HEIGHT = 30
START_Y_PADDING = 10
BOTTOM_BAR_HEIGHT = 40
BOTTOM_BAR_Y_PADDING = 5
BOTTOM_BAR_X_PADDING = 10
BOTTOM_BAR_ENTRY_X_PADDING = 5
BUBBLE_Y_PADDING = 10
BUBBLE_X_PADDING = 10
TEXT_Y_PADDING = 15
TEXT_X_PADDING = 10
ICON_X_PADDING = 0
HOVER_WIDTH = 5
ACTION_ICON_PADDING = 5
MESSAGE_BORDER_WIDTH = 2


class NotesFrame(ttk.Labelframe):
    def __init__(self, parent: ttk.Frame, app, project):
        ttk.Labelframe.__init__(
            self, parent, text="Notes", style="HugeBold.TLabelframe"
        )
        self.app = app
        self.project = project
        self.canvas_scroller = ScrolledCanvas(
            self, self.refresh, on_configure=self.refresh
        )
        self.canvas_scroller.place(relwidth=1, relheight=1, height=-BOTTOM_BAR_HEIGHT)
        self.canvas = self.canvas_scroller.canvas
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_click_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.trash_icon = tk.PhotoImage(file=get_asset("trash_32_black.png"))
        self.clicked_trash_icon = tk.PhotoImage(file=get_asset("trash_32_white.png"))

        self.copy_icon = tk.PhotoImage(
            file=get_asset("copy_clipboard_32_plain_black_bold_arrow.png")
        )
        self.clicked_copy_icon = tk.PhotoImage(
            file=get_asset("copy_clipboard_32_plain_white_bold_arrow.png")
        )

        self.on_note_left_click, self.on_note_right_click = None, None
        bottom_bar = ttk.Frame(self)
        bottom_bar.place(
            height=BOTTOM_BAR_HEIGHT, relwidth=1, rely=1, y=-BOTTOM_BAR_HEIGHT
        )

        self.entry = LabeledEntry(
            bottom_bar,
            labeltext="Add Note: ",
            bind_enter=True,
            command=self.add_note,
        )
        self.entry.pack(expand=True, fill="both", side=tk.LEFT)
        ttk.Button(
            bottom_bar,
            text="Submit",
            command=self.add_note,
        ).pack(fill="y", side=tk.RIGHT)
        self.refresh()

    def add_note(self, text=None):
        if not text:
            text = self.entry.get()
        if text:
            self.project.add_note(
                NoteEntry(
                    text,
                    time.time(),
                )
            )
        self.entry.clear()
        self.refresh()
        self.canvas.yview_moveto(1)

    def refresh(self, _=None, __=None):
        self.canvas.delete("all")
        self.width = self.canvas_scroller.winfo_width()
        running_total_height = START_Y_PADDING
        max_line_width = self.width - SCROLLBAR_WIDTH
        max_text_width = max_line_width - 2 * TEXT_X_PADDING
        for m in self.project.notes:
            text = self.canvas.create_text(
                BUBBLE_SIDE_SPACING,
                running_total_height + TEXT_Y_PADDING,
                text=m.content,
                fill="black",
                anchor="nw",
                width=max_text_width - BUBBLE_X_PADDING - TEXT_X_PADDING,
            )
            b = self.canvas.bbox(text)
            width, height = b[2] - b[0], b[3] - b[1]
            bg = self.canvas.create_round_rectangle(
                BUBBLE_SIDE_SPACING - TEXT_X_PADDING,
                running_total_height,
                max_line_width - TEXT_Y_PADDING,
                running_total_height + height + 3 * TEXT_Y_PADDING + 2,
                fill="#b1d5de",
                width=MESSAGE_BORDER_WIDTH,
            )
            b = self.canvas.bbox(bg)
            bg_width, bg_height = b[2] - b[0], b[3] - b[1]
            m.set_position(b[0], b[1], bg_width, bg_height)
            minsize = 2 * TEXT_Y_PADDING
            running_total_height += height if height > minsize else minsize
            running_total_height += 2 * TEXT_Y_PADDING + BUBBLE_Y_PADDING
            self.canvas.tag_raise(text)
            if m.active:
                self.activate_note(m)
        self.canvas_height = running_total_height
        self.canvas.config(
            scrollregion=(0, 0, running_total_height, running_total_height)
        )

    def deactivate_note(self, m):
        m.active = False
        for r in list(m.active_references.keys()):
            ref = m.active_references.pop(r)
            self.canvas.delete(ref)

    def activate_note(self, m):
        if m.active:
            self.deactivate_note(m)
        m.active = True

        trash = self.canvas.create_image(
            m.x + m.width - ACTION_ICON_PADDING,
            m.y + 2 * ACTION_ICON_PADDING,
            image=self.trash_icon,
            anchor="ne",
        )
        copy = self.canvas.create_image(
            *self.canvas.bbox(trash)[:2],
            image=self.copy_icon,
            anchor="ne",
        )

        datetime = self.canvas.create_text(
            m.x + m.width / 2,
            m.y + 1,
            text=get_friendly_time(int(m.timestamp), mode="all"),
            fill="black",
            anchor="n",
            font=self.app.small_bold_font,
        )
        m.active_references.update(
            {
                "trash": trash,
                "copy": copy,
                "outline": self.canvas.create_round_rectangle(
                    *m.bbox, width=HOVER_WIDTH
                ),
                "datetime": datetime,
            }
        )

    def _on_action(self, event, on_find_action=None):
        x, y = event.x, self.get_adjusted_y_view(event)
        found = False
        for n in self.project.notes:
            if not found:
                if n.is_in_range(x, y):
                    found = True
                    self.hovered = n
                    if not n.active:
                        self.activate_note(n)
                    if on_find_action:
                        on_find_action(n)
                else:
                    self.deactivate_note(n)
            else:
                self.deactivate_note(n)
        if not found:
            self.hovered = None

    def on_mouse_move(self, event):
        self._on_action(event)

    def on_left_click(self, event):  # Override superclass
        pos = event.x, self.get_adjusted_y_view(event)

        def on_left_click(note):  # If a note was clicked, check its subregions
            m = note
            if m.active_references.get("trash") and check_in_bounds(
                pos, self.canvas.bbox(m.active_references["trash"])
            ):
                ref = m.active_references.pop("trash")
                self.canvas.delete(ref)
                m.active_references["trash"] = self.canvas.create_image(
                    m.x + m.width - ACTION_ICON_PADDING,
                    m.y + 2 * ACTION_ICON_PADDING,
                    image=self.clicked_trash_icon,
                    anchor="ne",
                )
                self.project.delete_note(note)
            elif m.active_references.get("copy") and check_in_bounds(
                pos, self.canvas.bbox(m.active_references["copy"])
            ):
                ref = m.active_references.pop("copy")
                self.canvas.delete(ref)
                b = self.canvas.bbox(m.active_references["trash"])
                m.active_references["copy"] = self.canvas.create_image(
                    *b[:2],
                    image=self.clicked_copy_icon,
                    anchor="ne",
                )
                self.app.copy_to_user_clipboard(m.content)

        self._on_action(event, on_find_action=on_left_click)

    def on_left_click_release(self, event):
        self.refresh()

    def on_right_click(self, event):
        def on_right_click(note):
            if self.on_note_right_click:
                self.on_note_right_click(note)

        self._on_action(event, on_find_action=on_right_click)

    def get_adjusted_y_view(self, event):
        return int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
