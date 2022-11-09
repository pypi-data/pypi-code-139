# This file implements the install logic documented in Readme.md.
#
# It installs files *from* the `notebooks` directory juxtaposed with the
# location of this file, *to* the `exercises` directory juxtaposed with the
# `underactuated` package located with `import underacuated` (e.g. from your
# PYTHONPATH).

from importlib.util import find_spec
import json
import glob
import os
import errno
from itertools import filterfalse

manipulation_spec = find_spec('manipulation')
manipulation_root = os.path.dirname(os.path.dirname(
    manipulation_spec.origin)) + "/exercises"
solutions_root = os.path.dirname(os.path.abspath(__file__)) + "/notebooks"

print("This will 'install' " + solutions_root + " to " + manipulation_root + ", overwriting any previous contents.")
input("Press ENTER to continue...")

for filename in glob.glob(solutions_root + '/**/*.ipynb', recursive=True):
    print("-- Installing: " + os.path.basename(filename))
    install_file = str(filename).replace(solutions_root, manipulation_root)
    try:
        os.makedirs(os.path.dirname(install_file))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
    ipynb = json.load(open(filename))
    remove = lambda cell: "tags" in cell["metadata"] and "remove" in cell["metadata"]["tags"]
    ipynb["cells"] = list(filterfalse(remove, ipynb["cells"]))
    for cell in ipynb["cells"]:
        if "tags" in cell["metadata"] and "empty" in cell["metadata"]["tags"]:
            cell["source"] = []
    json.dump(ipynb, open(install_file, 'w'), indent=1)

for filename in glob.glob(solutions_root + '/**/*.bazel', recursive=True):
    install_file = str(filename).replace(solutions_root, manipulation_root)
    with open(filename, "r") as input:
        with open(install_file, "w") as output:
            for line in input:
                if 'grader_throws' not in line:
                    output.write(line)
