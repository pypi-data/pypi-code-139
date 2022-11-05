import os
import sys
from pathlib import Path

import numpy as np

from grid_table_py.support.table_ingest import interpret_table_from_snippet


def grid_table_py(path, outpath):
    out_path = Path(outpath)
    if not os.path.exists(path):
        print("Please provide a valid path to a md file")
        exit(1)
    if not os.path.exists(outpath):
        out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    out = []
    table_builders = interpret_table_from_snippet(text, out)
    out = np.array(out[0].split('\n'))
    for i in range(len(table_builders)):
        builder = table_builders[i]
        marker = f"++TABLE++{i}++"
        idx = -1
        for j in range(out.shape[0]):
            if f"++TABLE++{i}++" in out[j]:
                idx = j
                break

        if idx != -1:
            if out[idx].startswith(">"):
                prefix = out[idx].split()[0] + " "
                content = builder.to_grid_table(table_width=80 - len(prefix))
                for j in range(len(content)):
                    content[j] = prefix + content[j]
            else:
                content = builder.to_grid_table(table_width=80)
            if idx != out.shape[0]:
                out = np.concatenate((out[:idx], content, out[idx + 1:]))
            else:
                out = np.concatenate((out, content))

    out = "\n".join(out)

    if out_path.exists():
        with open(out_path, "w", encoding="utf-8") as outfile:
            outfile.write(out)
    else:
        with open(out_path, "x", encoding="utf-8") as outfile:
            outfile.write(out)


def run():
    if len(sys.argv) < 3:
        print("Requires two path arguments to input and output markdown files")
        exit(1)
    path = sys.argv[1]
    outpath = sys.argv[2]
    grid_table_py(path, outpath)