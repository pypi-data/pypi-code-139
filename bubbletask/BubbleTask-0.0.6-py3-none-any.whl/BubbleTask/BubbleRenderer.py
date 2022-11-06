import os, time, ctypes
import tkinter as tk
from tkinter import ttk
from threading import Thread

from py_simple_ttk import force_aspect, get_asset, hex_to_rgb, LabeledScale, hex_to_rgba

from PIL import Image, ImageDraw, ImageTk, ImageFont, ImageFilter

RADIUS = 150
TASK_RADIUS = 80
FONT = ImageFont.truetype(
    get_asset("fonts/Open_Sans/static/OpenSans/OpenSans-Bold.ttf"), 40
)
BACKGROUND_IMAGE = "./background_image.png"


def set_background(file: str):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(file), 0)


class SetBackground(Thread):
    def __init__(self, image: Image, update_action=None):
        Thread.__init__(self)
        self.image = image
        self.update_action = update_action

    def run(self):
        self.image.save(BACKGROUND_IMAGE)
        set_background(BACKGROUND_IMAGE)
        if self.update_action:
            update_action(self.image)


class BubbleRenderer:
    def __init__(self, app, resolution: tuple = (1920, 1080)):
        self.frame = 0
        self.app, self.resolution = app, resolution
        self.last_background = None
        self.background_image = None
        self.last_image = None
        # self.font_cache = {}

    def draw_ratio_circle(
        self,
        ratios,
        text,
        color,
        overdue_color,
        outline_color,
        outline_thickness,
        text_color,
        text_size,
        sunset_mode,
        turn_red,
        radius,
        # draw,
        # text_draw,
        draw_list,
        text_draw_list,
    ):
        if ratios[1] == -1:
            return
        diameter = 2 * radius

        self.adjusted_resolution = list(i for i in self.resolution)
        self.adjusted_resolution[1] = self.resolution[1] - diameter

        l = (r := ratios[0] * self.resolution[0] + radius) - diameter
        col = hex_to_rgba(color)
        if ratios[1] >= 1:
            if turn_red:
                col = hex_to_rgba(overdue_color)
            if not sunset_mode:
                t = (b := self.adjusted_resolution[1] - 1) - diameter
            else:
                t = (b := ratios[1] * self.adjusted_resolution[1]) - diameter
        else:
            t = (b := ratios[1] * self.adjusted_resolution[1]) - diameter
        t += diameter
        b += diameter

        draw_list.append(
            (
                ((int(l), int(t), int(r), int(b)),),
                {
                    "fill": tuple(col),
                    "outline": tuple(hex_to_rgba(outline_color)),
                    "width": int(outline_thickness),
                },
            )
        )
        x = int((l + r) / 2)
        y = int((t + b) / 2)

        font = ImageFont.truetype(
            get_asset("fonts/Open_Sans/static/OpenSans/OpenSans-Bold.ttf"),
            int(float(text_size)),
        )

        text_draw_list.append(
            (
                ((x, y), text),
                {
                    "fill": tuple(hex_to_rgba(text_color)),
                    "font": font,
                    "anchor": "mm",
                    "spacing": 0,
                    "align": "center",
                },
            )
        )

        return x, y

    def _draw_task(
        self,
        project,
        task,
        ratios: tuple,
        task_bubbles: list,
        task_texts: list,
    ):
        prof = self.app.profiles.current_profile
        return self.draw_ratio_circle(
            ratios,
            task.name,
            project.meta["task_bubble_color"],
            project.meta["task_overdue_color"],
            project.meta["task_outline_color"],
            project.meta["task_outline_thickness"],
            project.meta["task_text_color"],
            project.meta["task_text_size"],
            prof.get_preference("sunset_mode"),
            prof.get_preference("turn_red"),
            int(project.meta["task_radius"]),
            # self.task_draw,
            # self.task_text_draw,
            task_bubbles,
            task_texts,
        )

    def _draw_project(
        self,
        project,
        ratios: tuple,
        index: int,
        force: bool,
        project_bubbles: list,
        project_texts: list,
        task_bubbles: list,
        task_texts: list,
    ):
        prof = self.app.profiles.current_profile
        proj_width = self.resolution[0] / len(self.app.projects_tab.projects)
        start = (index - 1) * proj_width
        end = (index) * proj_width
        bubble_x = (start + end) / 2
        col = hex_to_rgba(project.meta["background_color"])
        self.bg_draw.rectangle((start, 0, end, self.resolution[1]), fill=tuple(col))

        center = self.draw_ratio_circle(
            (bubble_x / self.resolution[0], ratios[1]),
            project.name,
            project.meta["bubble_color"],
            project.meta["bubble_overdue_color"],
            project.meta["bubble_outline_color"],
            project.meta["bubble_outline_thickness"],
            project.meta["text_color"],
            project.meta["bubble_text_size"],
            prof.get_preference("sunset_mode"),
            prof.get_preference("turn_red"),
            int(project.meta["bubble_radius"]),
            # self.projects_draw,
            # self.projects_text_draw,
            project_bubbles,
            project_texts,
        )

        centers = []
        task_count = len(project.tasks)
        if not task_count:
            return
        width_per_task = (end - start) / task_count
        now, i = time.time(), 1
        for t in project.tasks:
            if t.last_update + t.update_delay < now or force:
                y_ratio = t.stat()
                t.last_update = now
            else:
                y_ratio = t.last_position
            t.last_position = y_ratio
            x_start = i * width_per_task - 0.5 * width_per_task + start
            i += 1
            centers.append(
                self._draw_task(
                    project,
                    t,
                    (x_start / self.resolution[0], y_ratio),
                    task_bubbles,
                    task_texts,
                )
            )
        return (center, centers)

    def make_image(self, force=False) -> Image:
        prof = self.app.profiles.current_profile

        kwargs = {
            "size": self.resolution,
            "color": (0, 0, 0, 0),
            "mode": "RGBA",
        }

        if bg := prof.get_preference("background_image"):
            if not bg == self.last_background:
                try:
                    self.background_image = (
                        Image.open(bg).convert("RGBA").resize(self.resolution)
                    )
                    self.last_background = bg
                    print(f"Loaded new background {bg}")
                except:
                    print("Failed to find background image. ")
                    prof.set_preference("background_image", "")
                    self.last_background = ""
                    self.background_image = Image.new(**kwargs)
        else:
            if not self.background_image:
                self.background_image = Image.new(**kwargs)

        self.bg_image = Image.new(**kwargs)
        self.bg_draw = ImageDraw.Draw(self.bg_image)

        canvas_width, canvas_height = self.resolution

        division_count = len(self.app.projects_tab.projects) - 1
        width_per_project = canvas_width
        if division_count:
            width_per_project /= division_count
        i = 0
        lines_to_draw = []
        project_bubbles = []
        project_texts = []
        task_bubbles = []
        task_texts = []
        projects = self.app.projects_tab.projects
        for p in projects:
            if float(p.last_update) + float(p.update_delay) < time.time() or force:
                y_ratio = p.stat()
                p.last_update = time.time()

            else:
                y_ratio = p.last_position
            p.last_position = y_ratio
            x_start = i * width_per_project
            i += 1
            lines_to_draw.append(
                self._draw_project(
                    p,
                    (x_start / canvas_width, y_ratio),
                    i,
                    force,
                    project_bubbles,
                    project_texts,
                    task_bubbles,
                    task_texts,
                )
            )

        i = 0
        out_image = self.background_image.copy()
        out_image.paste(self.bg_image, (0, 0), self.bg_image)
        for centers, project in zip(lines_to_draw, projects):
            width = int(self.resolution[0] / len(projects))
            line_image = Image.new(
                size=((width), self.resolution[1]), mode="RGBA", color=(0, 0, 0, 0)
            )
            line_draw = ImageDraw.Draw(line_image)
            if centers:
                center, task_centers = centers
                if task_centers:
                    for c in task_centers:
                        c = c[0] - i * width, c[1]
                        line_draw.line(
                            (center[0] - i * width, center[1], c),
                            fill=tuple(hex_to_rgba(project.meta["line_color"])),
                            width=int(float(project.meta["line_thickness"])),
                        )
            blur = int(project.meta["line_blur"])
            line_image = line_image.filter(ImageFilter.GaussianBlur(radius=blur))
            pos = ((i * width), 0)
            out_image.paste(line_image, pos, line_image)
            i += 1

        task_image = Image.new(**kwargs)
        task_draw = ImageDraw.Draw(task_image)
        for b in task_bubbles:
            args, kw = b
            task_draw.ellipse(*args, **kw)
        task_image = task_image.filter(ImageFilter.GaussianBlur(radius=2))
        task_draw = ImageDraw.Draw(task_image)
        for t in task_texts:
            args, kw = t
            task_draw.text(*args, **kw)

        bubble_image = Image.new(**kwargs)
        bubble_draw = ImageDraw.Draw(bubble_image)
        for b in project_bubbles:
            args, kw = b
            bubble_draw.ellipse(*args, **kw)
        bubble_image = bubble_image.filter(ImageFilter.GaussianBlur(radius=2))
        bubble_draw = ImageDraw.Draw(bubble_image)
        for t in project_texts:
            args, kw = t
            bubble_draw.text(*args, **kw)

        ##        out_image = self.background_image.copy()
        ##        out_image.paste(self.bg_image, (0, 0), self.bg_image)
        ##        out_image.paste(line_image, (0, 0), line_image)
        out_image.paste(task_image, (0, 0), task_image)
        out_image.paste(bubble_image, (0, 0), bubble_image)

        return out_image

    def get_frame(self, force=False) -> tuple:
        self.frame += 1
        return (self.make_image(force), self.frame - 1)


class BubbleViewer(ttk.Frame):
    def __init__(self, parent, renderer, update_delay, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.renderer = renderer
        self.image = None
        self.width, self.height = renderer.resolution
        self.update_delay = update_delay

        self.outer_frame = ttk.Frame(self)
        self.outer_frame.pack(side="top", fill="both", expand=True, padx=4, pady=4)
        self.outer_frame.config(width=250, height=200)
        self.inner_frame = ttk.Frame(self)
        force_aspect(
            self.inner_frame, self.outer_frame, float(self.width) / float(self.height)
        )

        self.canvas = tk.Canvas(self.inner_frame, relief="sunken")
        self.canvas.config(
            width=50,
            height=50,
        )
        self.canvas.config()
        self.canvas_frame = ttk.Frame(
            self.canvas,
            border=0,
        )
        self.canvas.create_window(0, 0, window=self.canvas_frame, anchor="nw")
        self.canvas_frame.config(width=50, height=50)
        self.canvas.pack(fill="both", expand=True)
        self.update()

    def set_update_delay(self, delay: int):
        self.update_delay = delay

    def update(self, force=False, verbose=False, update_action=None):
        if verbose:
            t = time.time()
        self.raw_image, frame = self.renderer.get_frame(force)
        if verbose:
            print(f"Generate frame took {time.time()-t} seconds")
            t2 = time.time()
        self.image = ImageTk.PhotoImage(
            self.raw_image.resize(
                (self.inner_frame.winfo_width(), self.inner_frame.winfo_height()),
                Image.BOX,
            )
        )
        if verbose:
            print(f"Generate image took {time.time()-t2} seconds")
            t3 = time.time()
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        if verbose:
            print(f"Draw canvas took {time.time()-t3} seconds")

        SetBackground(self.raw_image, update_action).start()
