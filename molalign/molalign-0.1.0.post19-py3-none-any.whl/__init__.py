try:
    from .wrapper import Alignment
except ModuleNotFoundError:
    from os import path
    from shutil import copyfile
    from subprocess import Popen, PIPE, STDOUT
    rootdir = path.dirname(__file__)
    command = [path.join(rootdir, 'build.sh'), '-lpy']
    try:
        copyfile(path.join(rootdir, 'config', 'gnu.cfg'), path.join(rootdir, 'build.cfg'))
    except FileExistsError:
        pass
    with Popen(command, stdout=PIPE, stderr=STDOUT, bufsize=0) as p:
        for line in p.stdout:
            print(">>> " + line)

