import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfiledialog
from py_simple_ttk import App, Tab, FocusedToplevel, LabeledPathEntry, force_aspect
from PIL import Image, ImageTk

from .BubbleRenderer import BubbleRenderer, BubbleViewer


class SaveImageWindow(FocusedToplevel):
    def __init__(self, window, image):
        self.image = image
        self.tk_image = ImageTk.PhotoImage(image=self.image)

        FocusedToplevel.__init__(self, window=window)
        self.geometry("500x400")

        self.entry = LabeledPathEntry(
            self.frame,
            "Select path to save file.",
            dialog=tkfiledialog.asksaveasfilename,
        )
        self.entry.pack(fill="x", expand=True, padx=20)

        self.outer_frame = ttk.Frame(self.frame)
        self.outer_frame.pack(side="top", fill="both", expand=True, padx=4, pady=4)
        self.outer_frame.config(width=250, height=200)
        self.inner_frame = ttk.Frame(self.frame)

        w, h = self.image.size
        force_aspect(self.inner_frame, self.outer_frame, w / h)

        self.canvas = tk.Canvas(self.inner_frame, relief="sunken")
        self.canvas.config(width=50, height=50)
        self.canvas_frame = ttk.Frame(self.canvas, border=0)
        self.canvas.create_window(0, 0, window=self.canvas_frame, anchor="nw")
        self.canvas_frame.config(width=50, height=50)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_configure, add="+")

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side=tk.TOP, fill="x", expand=True, padx=10)

        button = ttk.Button(button_frame, text="Cancel", command=self._on_cancel)
        button.pack(side=tk.LEFT, expand=True, fill="x")

        button = ttk.Button(button_frame, text="Save", command=self._on_yes)
        button.pack(side=tk.LEFT, expand=True, fill="x")

        self._finish_setup()

    def _on_yes(self, event=None):
        self.image.save(self.entry.get())
        self.destroy()

    def _on_cancel(self, event=None):
        self.destroy()

    def _on_configure(self, event=None):
        image = self.image
        aspect = float(image.width / float(image.height))
        self.temp_image = image.resize(
            (self.inner_frame.winfo_width(), self.inner_frame.winfo_height()),
            Image.Resampling.BOX,
        )
        self.temp_image = ImageTk.PhotoImage(self.temp_image)
        self.canvas.delete("all")
        self.canvas.create_image(
            self.inner_frame.winfo_width() // 2,
            self.inner_frame.winfo_height() // 2,
            image=self.temp_image,
            anchor="center",
        )


class ViewerTab(Tab):
    def __init__(self, app: App):
        Tab.__init__(self, app.notebook, "Viewer")
        self.renderer = BubbleRenderer(app, (1920, 1080))
        self.app = app
        self.viewer = BubbleViewer(
            self,
            self.renderer,
            int(
                float(
                    app.profiles.current_profile.get_preference("global_update_delay")
                    * 1000
                )
            ),
        )
        self.viewer.pack(fill="both", expand=True)
        app.profiles.add_select_profile_action(self.update_renderer_frequency)

        menu = tk.Menu(self.app.menu, tearoff=0)
        menu.add_command(label="Refresh", command=self.refresh)
        menu.add_command(label="Export Preview", command=self.export)
        app.menu.add_cascade(menu=menu, label="Viewer")

    def update_renderer_frequency(self, event=None):
        self.viewer.set_update_delay(
            float(
                self.app.profiles.current_profile.get_preference("global_update_delay")
                * 1000
            )
        )

    def export(self, event=None):
        def save(image):
            SaveImageWindow(self.winfo_toplevel(), image)

        self.viewer.update(force=True, update_action=save)

    def refresh(self):
        self.viewer.update(force=True)
