# __init__.py
# Copyright (C) 2019 (gnyontu39@gmail.com) and contributors
#

import inspect
import os
import sys

__version__ = '0.0.6'

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
sys.path.append(real_path)
from mng import pkdump
from mng import pkload

__all__ = [name for name, obj in locals().items()
           if not (name.startswith('_') or inspect.ismodule(obj))]

