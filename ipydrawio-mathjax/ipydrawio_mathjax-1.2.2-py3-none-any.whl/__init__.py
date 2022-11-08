"""MathJax for ipydrawio"""

# Copyright 2022 ipydrawio contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ipydrawio import _ipydrawio_labextension_paths

from ._version import __ext__, __js__, __prefix__, __version__


def _jupyter_labextension_paths():
    """static paths to link for interactive installation"""
    exts = _ipydrawio_labextension_paths(prefix=__prefix__, extensions=__ext__)
    return exts


__all__ = [
    "__js__",
    "__version__",
    "_jupyter_labextension_paths",
]
