import os, time
import tkinter as tk
from tkinter import ttk
from py_simple_ttk import Tab, get_unix_timestring, YesNoCancelWindow, PromptWindow

from .BubbleLib import Project, LoadedProject, get_projects_list
from .ProjectTab import ProjectTab
from .StartEndNameWindow import NewProjectWindow


class ProjectsTab(Tab):
    def __init__(self, app):
        self.app = app
        Tab.__init__(self, app.notebook, "Projects")
        self.toplevel = None
        self.projects = self._load_projects()
        project_menu = tk.Menu(self.app.menu, tearoff=0)
        project_menu.add_command(label="New Project", command=self._new_project)
        self.app.menu.add_cascade(menu=project_menu, label="Projects")

    def _load_projects(self) -> list:
        self.tabs = {}
        if hasattr(self, "notebook"):
            self.notebook.destroy()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        projects = []
        for path in get_projects_list():
            project = LoadedProject(self, path)
            self.tabs[project] = ProjectTab(self.notebook, self.app, self, project)
            projects.append(project)
        self.app.window.update_idletasks()
        self.app.use_theme(self.app.current_theme)
        return projects

    def _new_project(self, event=None) -> None:
        def start_new_project(*args, **kwargs):
            self._toplevel_destroy()
            self.start_new_project(*args, **kwargs)

        self.toplevel = NewProjectWindow(self.app.window, start_new_project)

    def start_new_project(self, title: str, start: float, deadline: float) -> Project:
        timestamp = get_unix_timestring()
        prof = self.app.profiles.current_profile
        project = Project(
            {
                "name": title,
                "start": start,
                "deadline": deadline,
                "atomic": str(time.time_ns()),
                "update_delay": prof.get_preference("default_update_delay"),
                "bubble_color": prof.get_preference("bubble_color"),
                "bubble_overdue_color": prof.get_preference("bubble_overdue_color"),
                "bubble_opacity": prof.get_preference("bubble_opacity"),
                "bubble_radius": prof.get_preference("bubble_radius"),
                "bubble_text_size": prof.get_preference("bubble_text_size"),
                "text_color": prof.get_preference("text_color"),
                "task_bubble_color": prof.get_preference("task_bubble_color"),
                "task_overdue_color": prof.get_preference("task_overdue_color"),
                "task_bubble_opacity": prof.get_preference("task_bubble_opacity"),
                "task_text_color": prof.get_preference("task_text_color"),
                "task_radius": prof.get_preference("task_radius"),
                "task_text_size": prof.get_preference("task_text_size"),
                "line_color": prof.get_preference("line_color"),
                "line_opacity": prof.get_preference("line_opacity"),
                "line_thickness": prof.get_preference("line_thickness"),
                "line_blur": prof.get_preference("line_blur"),
                "bubble_outline_color": prof.get_preference("bubble_outline_color"),
                "bubble_outline_opacity": prof.get_preference("bubble_outline_opacity"),
                "task_outline_color": prof.get_preference("task_outline_color"),
                "task_outline_opacity": prof.get_preference("task_outline_opacity"),
                "background_opacity": prof.get_preference("background_opacity"),
                "background_color": prof.get_preference("background_color"),
                "bubble_outline_thickness": prof.get_preference(
                    "bubble_outline_thickness"
                ),
                "task_outline_thickness": prof.get_preference("task_outline_thickness"),
                "tasks": [],
                "notes": [],
            }
        )
        project.save()
        last_tab = self.notebook.index("end")
        self.tabs[project] = ProjectTab(
            self.notebook,
            self.app,
            self,
            project,
        )
        self.projects.append(project)
        self.app.use_theme(self.app.current_theme)
        self.notebook.select(last_tab)
        self.app.notebook.select(self.app.notebook.index(self))
        return project

    def _toplevel_destroy(self, *args) -> None:
        """Function for toplevels to call on no / cancel"""
        self.toplevel.destroy()

    def rename_project(self, project) -> None:
        tab = self.tabs[project]

        def do_rename(new_name):
            if not new_name:
                self.toplevel.label_var.set("Enter valid project title")
                return
            tab.rename_project(new_name)
            self.toplevel.destroy()

        self.toplevel = PromptWindow(
            window=self.app.window,
            text="Enter New Project Name:",
            yes_text="Rename",
            on_yes=do_rename,
            on_cancel=self._toplevel_destroy,
            no_destroy=True,
        )

    def delete_project(self, project):
        tab = self.tabs[project]

        def do_delete(event=None):
            project.delete()
            self.projects = self._load_projects()
            self.toplevel.destroy()

        self.toplevel = YesNoCancelWindow(
            window=self.app.window,
            text=f'Are you sure you want to delete "{project.name}" ?',
            on_yes=do_delete,
            on_cancel=self._toplevel_destroy,
            yes_text="Confirm Delete",
            no_destroy=True,
            no_enabled=False,
        )
