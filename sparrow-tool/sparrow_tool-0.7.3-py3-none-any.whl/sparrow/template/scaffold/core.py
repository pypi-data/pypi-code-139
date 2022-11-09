from sparrow.template.core import Substituter
from sparrow.path import rel_to_abs
from pathlib import Path
from rich import print
import os


def gen_project(project_name="my_project", out_dir="./out", stdout=True):
    src_path = rel_to_abs('src', return_str=False)
    out_path = Path(out_dir)
    substituter = Substituter(stdout=stdout)
    substituter.render(src_path,
                       out_path.absolute(),
                       substitutions={"project_name": project_name},
                       exclude=[".so", ".pyc"]
                       )
    substituter.render_dir(os.path.join(out_path, "project_name"),
                           os.path.join(out_path, project_name))
    print(f"project generate success! Dir:\n {out_path.absolute()}")


if __name__ == "__main__":
    gen_project()
