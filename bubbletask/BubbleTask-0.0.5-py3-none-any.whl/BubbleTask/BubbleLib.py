import os, time, json, datetime

PROJECTS_FOLDER = os.path.abspath("Projects")
PROJECT_FILE_ENDING = "_meta.json"

os.makedirs(PROJECTS_FOLDER, exist_ok=True)

PROJECT_DEFAULTS = {
    "bubble_radius": 150,
    "task_radius": 75,
    "bubble_overdue_color": "#FF647FCC",
    "task_overdue_color": "#FF647FCC",
    "line_thickness": 4,
    "line_blur": 2,
    "line_color": "#00000000",
    "background_color": "#00000000",
    "bubble_outline_color": "#CCCCCCFF",
    "task_outline_color": "#CCCCCCFF",
    "task_outline_thickness": 3,
    "bubble_outline_thickness": 3,
    "bubble_text_size": 40,
    "task_text_size": 32,
    "notes": [],
    "tasks": [],
}


def parsetimes(in_date: str, in_time: list) -> float:
    m, d, y = in_date.split("/")
    h, mi, _ = in_time
    date = datetime.datetime.combine(
        datetime.date(int("20" + y), int(m), int(d)), datetime.time(int(h), int(mi))
    )
    return date.timestamp()


def get_projects_list(
    target: str = PROJECTS_FOLDER, end: str = PROJECT_FILE_ENDING
) -> list:
    """Gets a list of paths to note files from the Notes diretory."""
    projects = []
    for entry in os.scandir(target):
        if entry.is_file() and entry.path.endswith(end):
            projects.append(entry.path)
    return projects


class Note:
    def __init__(self, content: str, timestamp: float):
        self.content = content
        self.timestamp = timestamp

    def to_json(self) -> dict:
        return {
            "content": self.content,
            "timestamp": self.timestamp,
        }


class Task:
    def __init__(
        self,
        name: str,
        start: float,
        deadline: float,
        atomic: str = None,
        update_delay: float = 0.5,
    ):
        self.name, self.start, self.deadline = name, start, deadline
        self.atomic = atomic or time.time()
        self.update_delay = update_delay
        self.last_update = time.time() - self.update_delay
        self.last_position = None

    def to_json(self) -> dict:
        return {
            "atomic": self.atomic,
            "name": self.name,
            "start": self.start,
            "deadline": self.deadline,
            "update_delay": self.update_delay,
        }

    def stat(self) -> float:
        amount = self.deadline - self.start
        elapsed = time.time() - self.start
        return elapsed / amount


class CanvasElement:
    """Adds attributes to an element for use on a canvas"""

    def __init__(self):
        self.active = False
        self.references, self.active_references = [], {}
        self.x, self.y, self.width, self.height = 0, 0, 0, 0
        self.bbox = (0, 0, 0, 0)

    def set_position(self, x, y, width, height) -> None:
        self.x, self.y, self.width, self.height = x, y, width, height
        self.bbox = (self.x, self.y, self.x + self.width, self.y + self.height)

    def is_in_range(self, x, y) -> bool:
        l, t, r, b = self.bbox
        return all((x > l, x < r, y > t, y < b))


class TaskEntry(Task, CanvasElement):
    def __init__(
        self, name: str, start: float, deadline: float, atomic: str, update_delay: float
    ):
        CanvasElement.__init__(self)
        Task.__init__(self, name, start, deadline, atomic, update_delay)


class NoteEntry(Note, CanvasElement):
    def __init__(self, content: str, timestamp: float):
        CanvasElement.__init__(self)
        Note.__init__(self, content, timestamp)


class Project:
    """Core Project instance."""

    def __init__(
        self,
        metadata,
        # name: str,
        # start: float,
        # deadline: float,
        # atomic: str = None,
        # update_delay: float = 0.5,
        # bubble_color: str = None,
        # bubble_overdue_color: str = None,
        # bubble_opacity: int = None,
        # bubble_radius: int = None,
        # bubble_outline_color: str = None,
        # bubble_outline_opacity: int = None,
        # text_color: str = None,
        # task_bubble_color: str = None,
        # task_overdue_color: str = None,
        # task_bubble_opacity: int = None,
        # task_text_color: str = None,
        # task_radius: int = None,
        # task_outline_color: str = None,
        # task_outline_opacity: int = None,
        # line_color: str = None,
        # line_opacity: int = None,
        # line_thickness: int = None,
        # line_blur: int = None,
        # background_color: str = None,
        # background_opacity: str = None,
        tasks: list = [],
        notes: list = [],
        # metadata: dict,
    ):
        self.name = metadata.pop("name")
        self.tasks = tasks
        self.notes = notes
        self.update_delay = metadata.pop("update_delay")
        self.atomic = metadata.pop("atomic") or str(time.time_ns())
        self.path = os.path.join(PROJECTS_FOLDER, self.atomic + PROJECT_FILE_ENDING)
        self.start = metadata.pop("start")
        self.deadline = metadata.pop("deadline")
        self.meta = metadata

        # self.bubble_color = bubble_color
        # self.bubble_overdue_color = bubble_overdue_color
        # self.bubble_radius = bubble_radius
        # self.bubble_outline_color = bubble_outline_color
        # self.text_color = text_color
        # self.task_bubble_color = task_bubble_color
        # self.task_overdue_color = task_overdue_color
        # self.task_outline_color = task_outline_color
        # self.task_radius = task_radius
        # self.task_outline_color = task_outline_color
        # self.task_text_color = task_text_color
        # self.line_color = line_color
        # self.line_thickness = line_thickness
        # self.line_blur = line_blur
        # self.background_color = background_color

        self.last_update = time.time() - float(self.update_delay)
        self.last_position = None

    def add_task(self, task: Task) -> bool:
        self.tasks.append(task)
        return self.save()

    def delete_task(self, task: Task) -> bool:
        self.tasks.remove(task)
        return self.save()

    def add_note(self, note: Note) -> bool:
        self.notes.append(note)
        return self.save()

    def delete_note(self, note: Note) -> bool:
        self.notes.remove(note)
        return self.save()

    def save(self, path: str = None) -> bool:
        metadata = self.meta.copy()
        for k in ("tasks", "notes"):
            metadata.pop(k)
        metadata.update(
            {
                "atomic": self.atomic,
                "name": self.name,
                "start": self.start,
                "deadline": self.deadline,
                "update_delay": self.update_delay,
                # "bubble_color": self.bubble_color,
                # "bubble_overdue_color": self.bubble_overdue_color,
                # "bubble_opacity": self.bubble_opacity,
                # "bubble_radius": self.bubble_radius,
                # "bubble_outline_color": self.bubble_outline_color,
                # "bubble_outline_opacity": self.bubble_outline_opacity,
                # "text_color": self.text_color,
                # "task_bubble_color": self.task_bubble_color,
                # "task_overdue_color": self.task_overdue_color,
                # "task_bubble_opacity": self.task_bubble_opacity,
                # "task_text_color": self.task_text_color,
                # "task_radius": self.task_radius,
                # "task_outline_color": self.task_outline_color,
                # "task_outline_opacity": self.task_outline_opacity,
                # "line_thickness": self.line_thickness,
                # "line_blur": self.line_blur,
                # "line_opacity": self.line_opacity,
                # "line_color": self.line_color,
                # "background_color": self.background_color,
                # "background_opacity":self.background_opacity,
                "tasks": [t.to_json() for t in self.tasks],
                "notes": [n.to_json() for n in self.notes],
            }
        )
        try:
            with open(path or self.path, "w+") as f:
                json.dump(metadata, f)
            return True
        except:
            return False

    def rename(self, name: str) -> bool:
        """Returns false on invalid name"""
        if self.name:
            self.name = name
            return self.save()
        else:
            return False

    def delete(self) -> None:
        os.remove(self.path)

    def stat(self) -> float:
        try:
            amount = self.deadline - self.start
            elapsed = time.time() - self.start
            val = elapsed / amount
        except ZeroDivisionError:
            val = -1
        return val


class LoadedProject(Project):
    def __init__(self, taskstab, path):
        with open(path, "r") as f:
            meta = json.load(f)

        for k in PROJECT_DEFAULTS:
            if not k in meta:
                meta[k] = PROJECT_DEFAULTS[k]
        # if meta["task_radius"] is None:
        #     meta["task_radius"] = 150
        # if meta["bubble_radius"] is None:
        #     meta["bubble_radius"] = 75
        # if meta["background_color"] is None:
        #     meta["background_color"] = "#000000"
        # # if meta["background_opacity"] is None:
        # # meta["background_opacity"] = 0
        ##        if not meta["bubble_outline_color"]:
        ##            meta["bubble_outline_color"] = "#cccccc"
        # if not meta["task_outline_color"]:
        #     meta["task_outline_color"] = "#cccccc"
        # if not meta["bubble_outline_opacity"]:
        # meta["bubble_outline_opacity"] = 0
        # if not meta["task_outline_opacity"]:
        # meta["task_outline_opacity"] = 0

        Project.__init__(
            self,
            meta,
            tasks=[
                TaskEntry(
                    task_entry["name"],
                    task_entry["start"],
                    task_entry["deadline"],
                    task_entry["atomic"],
                    float(task_entry["update_delay"]),
                )
                for task_entry in meta["tasks"]
            ],
            notes=[
                NoteEntry(
                    note_entry["content"],
                    note_entry["timestamp"],
                )
                for note_entry in meta["notes"]
            ],
        )
