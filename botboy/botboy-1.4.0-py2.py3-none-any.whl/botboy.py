"""Multithreading & processing worker that executes functions and prints the result"""
__version__ = '1.4.0'

import threading
import multiprocessing

class BotBoy:
  def __init__(self, name, task):
    self.name = name
    self.task = task
    self.result = None
    self.processing = False
    self.on_file = False
    self.wait = False
    self.process = None
    self.thread = None

  def get_name(self):
    """Displays assigned name"""
    print(self.name)

  def get_task(self):
    """Displays current tasks"""
    print(self.task)

  def bot_task(self, *args):
    """Adds logging to the task"""
    print(f'{self.name} is executing task: {self.task}')

    self.result = self.task(*args)

    print(f'Retrieved result from {self.name}: {self.result}')

    if self.on_file:
      print('Storing result in file: result.txt')

      with open('result.txt', 'w') as f:
        f.write(f'{self.result}')

  def run_task_on_thread(self, *args):
    """Executes the task on a separate thread"""
    if self.thread: return

    self.thread = threading.Thread(target=self.bot_task, name=self.name, args=args)

    if self.wait:
      print(f'Waiting for {self.task} to finish')
      self.thread.run()
    else:
      self.thread.start()

    self.thread = None

  def run_task_on_process(self, *args):
    """Executes the task on a separate process"""
    if self.process: return

    self.process = multiprocessing.Process(target=self.bot_task, name=self.name, args=args)
    self.process.run()
    self.process = None

  def display_information(self):
    """Displays the bot's name and task"""
    self.get_name()
    self.get_task()

  def set_processing(self):
    """Changes from threading to processing"""
    if self.processing: self.processing = False
    else: self.processing = True

  def set_on_file(self):
    """Store result in file or not"""
    if self.on_file: self.on_file = False
    else: self.on_file = True

  def set_wait(self):
    """Waits for result or not"""
    if self.wait: self.wait = False
    else: self.wait = True

  def execute(self, *args):
    """Runs the assigned task"""
    if not self.processing: self.run_task_on_thread(*args)
    else: self.run_task_on_process(*args)

  def get_result(self):
    """Returns result from task execution"""
    return self.result

  def set_task(self, task):
    """Sets new task to run"""
    self.task = task
