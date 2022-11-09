import os
from solutions.docker_gradescope.problem_sets import current_problem_set


def docker_build():
    pset = current_problem_set()
    #command = 'docker build --build-arg drake_tag={} -t \
    #rachelholladay/manipulation21:{}-{} -f Dockerfile.ubuntu18.04 . '.format(
    #    pset.drake_tag, pset.drake_tag, pset.__class__.__name__)
    command = 'docker build --build-arg drake_tag={} -t \
        rachelholladay/manipulation21:{}-v1-{} -f Dockerfile.ubuntu18.04 . '.format(
        pset.drake_tag, pset.drake_tag, pset.__class__.__name__)
    print('Executing: ', command)
    os.system(command)


if __name__ == "__main__":
    docker_build()
