from os import system as sm


def install(lib_name, version=None):
    sm(f"pip install {lib_name + '==' + version if version else lib_name}")


def install_requirements(requirements_file_name):
    sm(f"pip install -r {requirements_file_name}")


def installs(*libs_name):
    r = " ".join([i for i in libs_name[0]]) if type(libs_name) == list else " ".join(libs_name)
    sm(f"pip install {r}")


def update(lib_name):
    sm(f"pip install -U {lib_name}")


def updates(*libs_name):
    sm(f"pip install -U {' '.join(libs_name)}")


def update_requirements(requirements):
    sm(f"pip install -U -r {requirements}")


def uninstall(lib_name):
    sm(f"pip uninstall -y {lib_name}")


def uninstalls(*libs_name):
    sm(f"pip uninstall -y {' '.join(libs_name)}")


def uninstall_requirements(requirements):
    sm(f"pip uninstall -y {requirements}")





