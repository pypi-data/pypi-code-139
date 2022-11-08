import logging
import os
import subprocess
import signal
from os import PathLike
from typing import Any, Union
from uuid import uuid4

from .. import socketio
from . import utils

class TaskElement():
    '''Represents one type of data to be displayed, keys should be unique identifiers.'''
    def __init__(self, id: str, name: str, task_id: str) -> None:
        super(TaskElement, self).__init__()
        self.id = id
        self.name = name
        self.task_id = task_id

    def __repr__(self) -> str:
        return 'Task Element'

class Alert(TaskElement):
    def __init__(self, id: str, name: str, task_id: str, msg:str="", state:str="primary") -> None:
        super().__init__(id, name, task_id)
        self.msg = msg
        self.state = state

    @property
    def component(self) -> str:
        return 'AlertElement'
    
    def struct(self) -> dict:
        return {"id": self.id, "name": self.name, "component": self.component, "state": self.state, "msg": self.msg}

    def set(self):
        pass

    def update(self):
        pass

class Progress(TaskElement):
    '''Signifies a Progress Bar.'''
    def __init__(self,
    id: str,
    name: str,
    task_id: str) -> None:
        super().__init__(id, name, task_id)
        # {'current' : x, 'max' : x}
        self.data = {"current": 0, "max": 1}

    @property
    def component(self) -> str:
        return 'ProgressElement'

    def struct(self) -> dict:
        return {"id": self.id, "name": self.name, "component": self.component}

    def set(self, value: dict) -> None:
        ''' set data to a new dictionary '''
        self.data = value
        self.update()

    def update(self) -> None:
        socketio.emit('progress_data_update', {self.id: self.data})

class Chart(TaskElement):
    ''' Signifies a plot on a 2D graph.'''
    def __init__(self,
    id: str,
    name: str,
    task_id: str,
    label_x: str = '',
    label_y: str = '') -> None:
        super().__init__(id, name, task_id)
        self.labels = {"label_x": label_x, "label_y": label_y}
        self.data = {"x": [], "y": []}

    @property
    def component(self) -> str:
        return 'ChartElement'

    def struct(self) -> dict:
        return {"id":self.id, "name": self.name, "component": self.component, "labels": self.labels}

    def set(self, value: dict) -> None:
        self.data = value
        self.update()
    
    def update(self) -> None:
        socketio.emit('chart_data_update', {self.id: self.data})

class Log(TaskElement):
    '''Signifies a console log - style scrolling output / text data'''
    def __init__(self,
    id: str,
    name: str,
    task_id: str) -> None:
        super().__init__(id, name, task_id)
        self.data = []

    @property
    def component(self) -> str:
        return 'LogElement'

    def struct(self) -> dict:
        return {"id": self.id, "name": self.name, "component": self.component}

    # XXX should be append, but doesn't play well with structure of other elements
    def set(self, value: str) -> None:
        ''' adds a log or list of logs to the end of the log '''
        if isinstance(value, list):
            self.data = self.data + value
        elif isinstance(value, str):
            self.data.append(value)
        self.update()

    def update(self) -> None:
        socketio.emit('log_data_update', {self.id: self.data})

class Gallery(TaskElement):
    '''Signifies an image gallery '''
    def __init__(self,
    id: str,
    name: str,
    task_id: str) -> None:
        super().__init__(id, name, task_id)
        # list of base64 encoded images
        self.data = []
        self.reference = []

    @property
    def component(self) -> str:
        return 'GalleryElement'

    def struct(self) -> dict:
        return {"id": self.id, "name": self.name, "component": self.component}

    # XXX should be append, but doesn't play well with structure of other elements
    def set(self, value: str) -> None:
        ''' appends the new image to the gallery '''
        if "data" in value:
            self.add_data(value["data"])
        elif "reference" in value:
            self.add_reference(value["reference"])

    def add_reference(self, value) -> None:
        self.reference.append(value)
        self.update()

    def add_data(self, value) -> None:
        self.data.append(value)
        self.update()

    def update(self) -> None:
        socketio.emit('gallery_data_update', {self.id: self.data})
        socketio.emit('gallery_reference_update', {self.id: self.reference})

components_class_dict = {
    'progress': Progress,
    'chart': Chart,
    'log': Log,
    'gallery': Gallery
}

# maps exit codes to alert components to show to the end user
exit_code_alerts_dict = {
    'success' : Alert(id="process_success_alert",
    name="Finished",
    task_id="UNIVERSAL",
    msg="Process completed successfully.",
    state="success"),
    'error' : Alert(id="process_error_alert",
    name="Error",
    task_id="UNIVERSAL",
    msg="Process closed unsuccessfully.",
    state="danger")
}
class Task():
    '''Represents one running process, id is a unique identifier for this task,
    mainly a list of task elements that compose the UI required by this process'''
    def __init__(self,
    id: str,
    struct: dict,
    launch_path: PathLike,
    launch_args: dict,
    root_path: PathLike) -> None:
        self.id = id
        self.active = True
        components = []
        name_id_map = {}
        for name, component in struct.items():
            component_id = str(uuid4())
            name_id_map[name] = component_id
            components.append(components_class_dict[component](id=component_id, name=name, task_id=id))
        self.components = components
        self.root_path = root_path
        args = [str(launch_path), "-id", id, "--rootpath", str(root_path)] + utils.parse_args(launch_args)
        self.process = subprocess.Popen(" ".join(args), shell=True, preexec_fn=os.setsid)

    def get_component(self, name: str) -> TaskElement:
        ''' get a component by its name '''
        for element in self.components:
            if element.name == name:
                return element
        return None

    def struct(self) -> dict:
        ''' returns the task's structure as a dictionary '''
        return {"id": self.id, "struct": [el.struct() for el in self.components], "active": self.active}

    def update_component(self, component_id: str) -> None:
        ''' Cause a component to send an update to the display'''
        try:
            self.get_component(id=component_id).update()
        except TypeError:
            logging.error(f'component with id {component_id} not found in task {self.id}')
    
    def write_component(self, name: str, value) -> None:
        ''' write a component's display data '''
        try:
            self.get_component(name).set(value)
        except TypeError:
            logging.error(f'component with name {name} not found in task {self.id}')
        
    def terminate_process(self) -> None:
        ''' kill the subprocess associated with this task '''
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

    def end(self) -> None:
        ''' mark this task as ended '''
        streamdata = self.process.communicate()
        # get the exit code
        exit_code = self.process.returncode
        logging.error(f'process closed with exit code {exit_code}')
        if exit_code == 0:
            # show success if closed successfully
            self.components.insert(0, exit_code_alerts_dict["success"])
        else:
            # show an error otherwise
            self.components.insert(0, exit_code_alerts_dict["error"])
        self.active = False
        
    def __repr__(self) -> str:
        return 'id: ' + self.id + 'struct: ' + " ".join(str(x) for x in self.components)

class TaskManager():
    ''' Manages the Tasks, manages the history of all the tasks that have been run this session,
     has a list of tasks and tasks can be retrieved through indexing '''
    def __init__(self) -> None:
        self.tasks = []

    def __getitem__(self, indices):
        return self.tasks.__getitem__(indices)

    def __repr__(self) -> Any:
        return self.tasks.__repr__()

    def create_task(self, id: str, struct: str, launch_path: PathLike, launch_args: dict, root_path: PathLike) -> None:
        ''' append a new task to the end or override an existing task if the id matches '''
        if self.get_by_id(id) is not None:
            # task id's should be unique, do not add if there is already a task with this id
            logging.error(f'a task with id: {id} already exists')
        else: 
            self.tasks.append(Task(
                id = id,
                struct = struct,
                launch_path = launch_path,
                launch_args = launch_args,
                root_path = root_path
            ))
            # update clients about task state
            socketio.emit('tasks', self.struct())
            socketio.emit('server_added_task', id)
            
    def terminate_task_process(self, id: str) -> None:
        '''close the process associated with a task.'''
        self.get_by_id(id).terminate_process()

    def end_task(self, task_id):
        ''' end a task '''
        self.get_by_id(task_id).end()
        self.export_struct()

    def get_by_id(self, id) -> Union[Task, None]:
        ''' return a Task by its id, returns '''
        for task in self.tasks:
            if task.id == id:
                return task
        return None

    def struct(self) -> list:
        ''' return a list of all the task dictionaries, representing the state of the entire system,
        in the structure required by the frontend to flow through the props in the vue components'''
        data = [task.struct() for task in self.tasks]
        return data

    def write_element(self, task_id: str, element_name: str, new_value: str) -> None:
        ''' Located the specified element by using its key an the id of the Task it is part of,
        then calls its set with the new value.'''
        try:
            self.get_by_id(task_id).write_component(element_name, new_value)
        except TypeError:
            logging.error(f'No Task with id {task_id} currently exists.')

    def update_component(self, update_request) -> None:
        ''' cause a targeted component to fire its update method '''
        for task in self.tasks:
            if task.id == update_request['task_id']:
                for component in task.components:
                    if component.name == update_request['component_name']:
                        component.update()
                        return None

    def export_struct(self) -> None:
        socketio.emit('tasks', self.struct())

tasks = TaskManager()
