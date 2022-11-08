from sparrow.template.core import Substituter
from sparrow.path import rel_to_abs, rel_path_join


def gen_project(project_name="my_project", out_dir="./out", stdout=True):
    src_path = rel_to_abs('src', return_str=False)
    out_path = rel_to_abs(out_dir, return_str=False)
    substituter = Substituter(stdout=stdout)
    substituter.render(src_path,
                       out_path,
                       substitutions={"project_name": project_name}
                       )
    substituter.render_dir(rel_path_join(out_dir, "project_name"),
                           rel_path_join(out_dir, project_name))


if __name__ == "__main__":
    gen_project(project_name="sparrow", out_dir="out")
