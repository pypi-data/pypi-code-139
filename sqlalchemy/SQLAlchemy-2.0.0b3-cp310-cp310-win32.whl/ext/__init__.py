# ext/__init__.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

from .. import util as _sa_util


_sa_util.preloaded.import_prefix("sqlalchemy.ext")
