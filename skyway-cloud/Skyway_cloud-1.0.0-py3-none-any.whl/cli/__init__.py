import os
import importlib

cli_path = os.path.dirname(__file__)
commands = {}

for f in os.listdir(cli_path):
    if f not in ['__init__.py', '__main__.py'] and f.endswith('.py'):
        module = f[:-3]
        commands[module] = importlib.import_module('skyway.cli.' + module)