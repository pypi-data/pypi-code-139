import time
import tkinter as tk
from tkinter import ttk

from py_simple_ttk import (
    App,
    Tab,
    LabeledEntry,
    ScrolledCanvas,
    get_asset,
    get_friendly_time,
    check_in_bounds,
)

from .BubbleLib import Project, TaskEntry, parsetimes
from .TimeSelectionButton import TimeSelectionButton
from .StartEndNameWindow import NewTaskWindow, EditTaskWindow

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


class TasksFrame(ttk.Labelframe):
    def __init__(self, parent, app: App, project: Project):
        ttk.Labelframe.__init__(
            self, parent, text="Tasks", style="HugeBold.TLabelframe"
        )
        self.app, self.project = app, project
        self.window, self.toplevel = app.window, None

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
        self.edit_icon = tk.PhotoImage(file=get_asset("pencil_32_black.png"))
        self.clicked_edit_icon = tk.PhotoImage(file=get_asset("pencil_32_white.png"))
        self.on_task_left_click = None
        self.on_task_right_click = None

        (bottom_bar := ttk.Frame(self)).place(
            height=BOTTOM_BAR_HEIGHT, relwidth=1, rely=1, y=-BOTTOM_BAR_HEIGHT
        )

        ttk.Button(
            bottom_bar,
            text="New Task",
            command=self.new_task,
        ).pack(fill="both", side=tk.TOP, expand=True)

        self.refresh()

    def add_task(self, name: str, start: float, deadline: float):
        self.project.add_task(
            TaskEntry(
                name,
                start,
                deadline,
                time.time(),
                self.app.profiles.current_profile.get_preference(
                    "default_update_delay"
                ),
            )
        )
        self.refresh()
        self.canvas.yview_moveto(1)

    def new_task(self) -> None:
        def new_task(*args, **kwargs):
            self.toplevel.destroy()
            self.add_task(*args, **kwargs)

        self.toplevel = NewTaskWindow(self.app.window, new_task)

    def edit_task(self, task) -> None:
        def edit_task(name, start, deadline):
            self.toplevel.destroy()
            task.name = name
            task.start = start
            task.deadline = deadline
            y_view = self.canvas.yview()
            self.refresh()
            self.canvas.yview_moveto(y_view[0])
            self.project.save()

        self.toplevel = EditTaskWindow(self.app.window, edit_task, task)

    def delete_task(self, task) -> None:
        self.project.delete_task(task)
        self.refresh()

    def start_new_project(self, title: str, start: float, deadline: float) -> Project:
        timestamp = get_unix_timestring()
        last_tab = self.notebook.index("end")
        project = Project(title, start, deadline)
        project.save()
        self.tabs[project] = ProjectTab(self.notebook, self.app, self, project)
        self.projects.append(project)
        self.app.use_theme(self.app.current_theme)
        self.notebook.select(last_tab)
        self.app.notebook.select(self.app.notebook.index(self))
        return project

    def refresh(self, _=None, __=None) -> None:
        self.canvas.delete("all")
        self.width = self.canvas_scroller.winfo_width()
        running_total_height = START_Y_PADDING
        max_line_width = self.width - SCROLLBAR_WIDTH
        max_text_width = max_line_width - 2 * TEXT_X_PADDING
        for m in self.project.tasks:
            name = self.canvas.create_text(
                BUBBLE_SIDE_SPACING,
                running_total_height + TEXT_Y_PADDING,
                text=m.name,
                fill="black",
                anchor="nw",
                width=max_text_width - BUBBLE_X_PADDING - TEXT_X_PADDING,
                font=self.app.large_bold_font,
            )
            b = self.canvas.bbox(name)
            width = b[2] - b[0]
            height_1 = b[3] - b[1]
            start_time_label = self.canvas.create_text(
                BUBBLE_SIDE_SPACING,
                running_total_height + height_1 + TEXT_Y_PADDING,
                text="Start: ",
                fill="black",
                anchor="nw",
                width=max_text_width - BUBBLE_X_PADDING - TEXT_X_PADDING,
                font=self.app.bold_font,
            )
            b = self.canvas.bbox(start_time_label)
            st_width = b[2] - b[0]
            start_time = self.canvas.create_text(
                BUBBLE_SIDE_SPACING + st_width,
                running_total_height + height_1 + TEXT_Y_PADDING,
                text=get_friendly_time(m.start),
                fill="black",
                anchor="nw",
                width=max_text_width - BUBBLE_X_PADDING - TEXT_X_PADDING,
            )
            b = self.canvas.bbox(start_time)
            width = b[2] - b[0]
            height_2 = b[3] - b[1]
            end_time_label = self.canvas.create_text(
                BUBBLE_SIDE_SPACING,
                running_total_height + height_1 + height_2 + TEXT_Y_PADDING,
                text="End: ",
                fill="black",
                anchor="nw",
                width=max_text_width - BUBBLE_X_PADDING - TEXT_X_PADDING,
                font=self.app.bold_font,
            )
            b = self.canvas.bbox(end_time_label)
            et_width = b[2] - b[0]
            end_time = self.canvas.create_text(
                BUBBLE_SIDE_SPACING + et_width,
                running_total_height + height_1 + height_2 + TEXT_Y_PADDING,
                text=get_friendly_time(m.deadline),
                fill="black",
                anchor="nw",
                width=max_text_width - BUBBLE_X_PADDING - TEXT_X_PADDING,
            )
            b = self.canvas.bbox(end_time)
            width = b[2] - b[0]
            height_3 = b[3] - b[1]
            height = height_1 + height_2 + height_3
            bg = self.canvas.create_round_rectangle(
                BUBBLE_SIDE_SPACING - TEXT_X_PADDING,
                running_total_height,
                max_line_width - TEXT_Y_PADDING,
                running_total_height + height + 2 * TEXT_Y_PADDING,
                fill="#b1d5de",
                width=MESSAGE_BORDER_WIDTH,
            )
            b = self.canvas.bbox(bg)
            bg_width, bg_height = b[2] - b[0], b[3] - b[1]
            m.set_position(b[0], b[1], bg_width, bg_height)
            minsize = 2 * TEXT_Y_PADDING
            running_total_height += height if height > minsize else minsize
            running_total_height += 2 * TEXT_Y_PADDING + BUBBLE_Y_PADDING
            self.canvas.tag_raise(name)
            self.canvas.tag_raise(start_time_label)
            self.canvas.tag_raise(start_time)
            self.canvas.tag_raise(end_time_label)
            self.canvas.tag_raise(end_time)
            if m.active:
                self.activate_task(m)
        self.canvas_height = running_total_height
        self.canvas.config(
            scrollregion=(0, 0, running_total_height, running_total_height)
        )

    def on_left_click(self, event) -> None:
        pos = event.x, self.get_adjusted_y_view(event)

        def on_left_click(task) -> None:  # If a task was clicked, check its subregions
            m = task
            print(m)
            if m.active_references.get("trash") and check_in_bounds(
                pos, self.canvas.bbox(m.active_references["trash"])
            ):
                ref = m.active_references.pop("trash")
                self.canvas.delete(ref)
                m.active_references["trash"] = self.canvas.create_image(
                    m.x + m.width - ACTION_ICON_PADDING,
                    m.y + ACTION_ICON_PADDING,
                    image=self.clicked_trash_icon,
                    anchor="ne",
                )
                self.delete_task(task)
            if m.active_references.get("edit") and check_in_bounds(
                pos, self.canvas.bbox(m.active_references["edit"])
            ):
                ref = m.active_references.pop("edit")
                b = self.canvas.bbox(ref)
                width, height = b[2] - b[0], b[3] - b[1]
                self.canvas.delete(ref)

                m.active_references["edit"] = self.canvas.create_image(
                    b[0] + width,
                    b[1],
                    image=self.clicked_edit_icon,
                    anchor="ne",
                )
                self.edit_task(task)
                self.after(100, self.refresh)

        self._on_action(event, on_find_action=on_left_click)

    def deactivate_task(self, m) -> None:
        m.active = False
        for r in list(m.active_references.keys()):
            ref = m.active_references.pop(r)
            self.canvas.delete(ref)

    def activate_task(self, m) -> None:
        if m.active:
            self.deactivate_task(m)
        m.active = True

        trash = self.canvas.create_image(
            m.x + m.width - ACTION_ICON_PADDING,
            m.y + ACTION_ICON_PADDING,
            image=self.trash_icon,
            anchor="ne",
        )
        b = self.canvas.bbox(trash)
        width, height = b[2] - b[0], b[3] - b[1]

        edit = self.canvas.create_image(
            m.x + m.width - ACTION_ICON_PADDING,
            m.y + height + ACTION_ICON_PADDING,
            image=self.edit_icon,
            anchor="ne",
        )

        datetime = self.canvas.create_text(
            m.x + m.width / 2,
            m.y + 1,
            text=f'Created {get_friendly_time(int(m.start), mode="all")}',
            fill="black",
            anchor="n",
            font=self.app.small_bold_font,
        )
        m.active_references.update(
            {
                "trash": trash,
                "edit": edit,
                "outline": self.canvas.create_round_rectangle(
                    *m.bbox, width=HOVER_WIDTH
                ),
                "datetime": datetime,
            }
        )

    def _on_action(self, event, on_find_action=None) -> None:
        x, y = event.x, self.get_adjusted_y_view(event)
        found = False
        for m in self.project.tasks:
            if not found:
                if m.is_in_range(x, y):
                    found = True
                    self.hovered = m
                    if not m.active:
                        self.activate_task(m)
                    if on_find_action:
                        on_find_action(m)
                else:
                    self.deactivate_task(m)
            else:
                self.deactivate_task(m)
        if not found:
            self.hovered = None

    def on_mouse_move(self, event) -> None:
        self._on_action(event)

    def on_left_click_release(self, event) -> None:
        self.refresh()

    def on_right_click(self, event) -> None:
        def on_right_click(task):
            if self.on_task_right_click:
                self.on_task_right_click(task)

        self._on_action(event, on_find_action=on_right_click)

    def get_adjusted_y_view(self, event) -> int:
        return int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
