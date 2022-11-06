from tkinter import ttk

from py_simple_ttk import (
    App,
    Tab,
    LabeledScale,
    LabeledFloatEntry,
    rgb_to_hex,
    hex_to_rgb,
)

from .BubbleLib import Project, parsetimes

from .TasksFrame import TasksFrame
from .NotesFrame import NotesFrame

from .TimeSelectionButton import TimeSelectionButton
from .ColorPickerButton import ColorPickerButton, ColorPickerButton2
from .Spinbox import LabeledSpinbox


class ProjectTab(Tab):
    def __init__(
        self,
        notebook: ttk.Notebook,
        app: App,
        projects_tab,
        project: Project,
    ):
        Tab.__init__(self, notebook, project.name)
        self.project = project
        self.projects_tab = projects_tab

        (header := ttk.Frame(self)).pack(fill="x", side="top", padx=(20))
        (header_left := ttk.Frame(header)).pack(fill="both", side="left", expand=False)

        def build_button_menu(title, options):
            (
                options_frame := ttk.Labelframe(
                    header_left, text=title, style="HugeBold.TLabelframe"
                )
            ).pack(side="top", fill="x", pady=0)
            for opt in options:
                title, action = opt
                ttk.Button(
                    options_frame,
                    text=title,
                    command=action,
                    padding=(0, 0),
                ).pack(
                    side="top",
                    padx=0,
                    pady=0,
                    fill="x",
                    expand=True,
                    # ipadx=0,
                    # ipady=0,
                )

        build_button_menu(
            "Project",
            (
                (
                    "Rename Project",
                    lambda: projects_tab.rename_project(project),
                ),
                # (
                #     "Copy Project",
                #     lambda: projects_tab.copy_project(project),
                # ),
                (
                    "Delete Project",
                    lambda: projects_tab.delete_project(project),
                ),
            ),
        )

        (
            times_frame := ttk.Labelframe(
                header_left, text="Times", style="HugeBold.TLabelframe"
            )
        ).pack(side="top", pady=0, anchor="n", fill="both", expand=True)

        self.start_button = TimeSelectionButton(
            times_frame,
            command=self.on_time_change,
            default=project.start,
            text="Start ",
        )
        self.start_button.pack(side="top", fill="x", anchor="n", expand=False)

        self.deadline_button = TimeSelectionButton(
            times_frame,
            command=self.on_time_change,
            default=project.deadline,
            text="Deadline ",
        )
        self.deadline_button.pack(side="top", fill="x", anchor="n", expand=False)

        self.entry = LabeledSpinbox(
            times_frame,
            "Update Freq:",
            command=self.on_frequency_update,
            default=str(project.update_delay),
            on_keystroke=True,
            from_=1,
            to=1000 * 1000,
            fill="x",
            expand=False,
        )

        self.entry.pack(side="top", fill="x")
        self.entry.set(project.update_delay)

        (
            colors_frame := ttk.Labelframe(
                header, text="Config", style="HugeBold.TLabelframe"
            )
        ).pack(side="right", fill="x", expand=True, pady=0, anchor="n")

        (colors_a := ttk.LabelFrame(colors_frame, text="Project")).pack(
            side="left", expand=True, fill="y"
        )
        (colors_b := ttk.LabelFrame(colors_frame, text="Task")).pack(
            side="left", expand=True, fill="y"
        )
        (colors_c := ttk.LabelFrame(colors_frame, text="Etc")).pack(
            side="left", expand=True, fill="y"
        )

        self.proj_bubble_color = ColorPickerButton2(
            colors_a,
            "Bubble Color",
            self.project.meta["bubble_color"],
            command=self.on_color_change,
        )
        self.proj_bubble_color.pack(fill="x", expand=True)

        self.proj_bubble_overdue_color = ColorPickerButton2(
            colors_a,
            "Overdue Color",
            self.project.meta["bubble_overdue_color"],
            command=self.on_color_change,
        )
        self.proj_bubble_overdue_color.pack(fill="x")

        self.proj_text_color = ColorPickerButton2(
            colors_a,
            "Text Color",
            self.project.meta["text_color"],
            command=self.on_color_change,
        )
        self.proj_text_color.pack(fill="x")

        self.proj_bubble_radius = LabeledSpinbox(
            colors_a,
            "Radius",
            command=self.on_color_change,
            from_=10,
            to=500,
            default=str(self.project.meta["bubble_radius"]),
            on_keystroke=True,
        )
        self.proj_bubble_radius.pack(fill="x")

        self.bubble_outline_color = ColorPickerButton2(
            colors_a,
            "Outline Color",
            self.project.meta["bubble_outline_color"],
            command=self.on_color_change,
        )
        self.bubble_outline_color.pack(fill="x")

        self.bubble_outline_thickness = LabeledSpinbox(
            colors_a,
            "Outline Width",
            command=self.on_color_change,
            from_=0,
            to=20,
            default=str(self.project.meta["bubble_outline_thickness"]),
            on_keystroke=True,
        )
        self.bubble_outline_thickness.pack(fill="x")

        self.bubble_text_size = LabeledSpinbox(
            colors_a,
            "Text Size",
            command=self.on_color_change,
            from_=12,
            to=200,
            default=str(self.project.meta["bubble_text_size"]),
            on_keystroke=True,
        )
        self.bubble_text_size.pack(fill="x")

        self.task_bubble_color = ColorPickerButton2(
            colors_b,
            "Bubble Color",
            command=self.on_color_change,
            default=self.project.meta["task_bubble_color"],
        )
        self.task_bubble_color.pack(fill="x")

        self.task_overdue_bubble_color = ColorPickerButton2(
            colors_b,
            "Task Color",
            command=self.on_color_change,
            default=self.project.meta["task_overdue_color"],
        )
        self.task_overdue_bubble_color.pack(fill="x")

        self.task_text_color = ColorPickerButton2(
            colors_b,
            "Text Color",
            command=self.on_color_change,
            default=self.project.meta["task_text_color"],
        )
        self.task_text_color.pack(fill="x")

        self.proj_task_radius = LabeledSpinbox(
            colors_b,
            "Radius",
            command=self.on_color_change,
            from_=10,
            to=500,
            default=str(self.project.meta["task_radius"]),
            on_keystroke=True,
        )
        self.proj_task_radius.pack(fill="x")

        self.task_outline_color = ColorPickerButton2(
            colors_b,
            "Outline Color",
            command=self.on_color_change,
            default=self.project.meta["task_outline_color"],
        )
        self.task_outline_color.pack(fill="x")

        self.task_outline_thickness = LabeledSpinbox(
            colors_b,
            "Outline Width",
            command=self.on_color_change,
            from_=0,
            to=20,
            default=str(self.project.meta["task_outline_thickness"]),
            on_keystroke=True,
        )
        self.task_outline_thickness.pack(fill="x")

        self.task_text_size = LabeledSpinbox(
            colors_b,
            "Text Size",
            command=self.on_color_change,
            from_=12,
            to=200,
            default=str(self.project.meta["task_text_size"]),
            on_keystroke=True,
        )
        self.task_text_size.pack(fill="x")

        self.line_color = ColorPickerButton2(
            colors_c,
            "Line Color",
            command=self.on_color_change,
            default=self.project.meta["line_color"],
        )
        self.line_color.pack(fill="x")

        self.line_thickness = LabeledSpinbox(
            colors_c,
            "Line Thickness",
            command=self.on_color_change,
            from_=0,
            to=7,
            default=str(self.project.meta["line_thickness"]),
            on_keystroke=True,
        )
        self.line_thickness.pack(fill="x")

        self.line_blur = LabeledSpinbox(
            colors_c,
            "Line Blur",
            command=self.on_color_change,
            from_=0,
            to=7,
            default=str(self.project.meta["line_blur"]),
            on_keystroke=True,
        )
        self.line_blur.pack(fill="x")

        self.background_color = ColorPickerButton2(
            colors_c,
            "Column Color",
            command=self.on_color_change,
            default=self.project.meta["background_color"],
        )
        self.background_color.pack(fill="x")

        (footer_frame := ttk.Frame(self)).pack(side="top", fill="both", expand=True)

        self.tasks_frame = TasksFrame(footer_frame, app, project)
        self.tasks_frame.pack(
            side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 0)
        )

        self.notes_frame = NotesFrame(footer_frame, app, project)
        self.notes_frame.pack(
            side="right", fill="both", expand=True, padx=(0, 20), pady=(0, 0)
        )

    def on_color_change(self, val: str) -> bool:
        self.project.meta["bubble_color"] = self.proj_bubble_color.get()
        self.project.meta["bubble_overdue_color"] = self.proj_bubble_overdue_color.get()
        self.project.meta["text_color"] = self.proj_text_color.get()
        self.project.meta["task_bubble_color"] = self.task_bubble_color.get()
        self.project.meta["task_overdue_color"] = self.task_overdue_bubble_color.get()
        self.project.meta["task_text_color"] = self.task_text_color.get()
        self.project.meta["line_thickness"] = self.line_thickness.get()
        self.project.meta["line_blur"] = self.line_blur.get()
        self.project.meta["line_color"] = self.line_color.get()
        self.project.meta["bubble_radius"] = self.proj_bubble_radius.get()
        self.project.meta["task_radius"] = self.proj_task_radius.get()
        self.project.meta["background_color"] = self.background_color.get()
        self.project.meta["bubble_outline_color"] = self.bubble_outline_color.get()
        self.project.meta[
            "bubble_outline_thickness"
        ] = self.bubble_outline_thickness.get()
        self.project.meta["task_outline_color"] = self.task_outline_color.get()
        self.project.meta["task_outline_thickness"] = self.task_outline_thickness.get()
        self.project.meta["bubble_text_size"] = self.bubble_text_size.get()
        self.project.meta["task_text_size"] = self.task_text_size.get()
        return self.project.save()

    def on_frequency_update(self, val: float) -> bool:
        if not val:
            return
        self.project.update_delay = val
        return self.project.save()

    def delete_task(self, task) -> None:
        self.project.delete_task(task)
        self.tasks_frame.refresh()

    def rename_project(self, name: str) -> None:
        self.projects_tab.notebook.tab(self, text=name)
        self.project.rename(name)

    def on_time_change(self, values: dict = None) -> bool:
        self.project.start = parsetimes(*self.start_button.get())
        self.project.deadline = parsetimes(*self.deadline_button.get())
        return self.project.save()
