import os.path

from colorama import init
from ppcmd.ppc.params import TgzParam

from ppcmd.common.date_format import cur_short_time_str
from ppcmd.common.exit_code import ExitCode, exit_with_error_msg
from ppcmd.common.print import print_major_cmd_step__
from ppcmd.common.run import run__


def init_ppc_pkg():
    init(autoreset=True)  # color auto reset


class PpcProcessor:
    def __init__(self):
        init_ppc_pkg()

    def tgz(self, param: TgzParam):
        if not os.path.exists(param.save_loc):
            exit_with_error_msg(ExitCode.FAILED_TO_TGZ__SAVE_LOC_DOES_NOT_EXIST)
        if not os.path.isdir(param.save_loc):
            exit_with_error_msg(ExitCode.FAILED_TO_TGZ__SAVE_LOC_IS_NOT_DIR)

        print_major_cmd_step__(f'tgz {param.src_dir}...')
        out_name = os.path.basename(param.src_dir) \
            if param.outfile_name == "" else param.outfile_name
        timestamp = f"{cur_short_time_str()}{param.custom_timestamp_suffix}"
        output_filename = f'{timestamp}__{out_name}.tgz' \
            if param.prefix_timestamp else f'{out_name}__{timestamp}.tgz'
        run__(f"tar cvzf {output_filename} {param.src_dir}")
        # with tarfile.open(output_filename, "w:gz") as tar:
        #     tar.add(dir, arcname=os.path.basename(dir))
        if param.save_loc == ".":
            run__(f"ls -lah {output_filename}")
        else:
            run__(f"mv {output_filename} {param.save_loc}")
            run__(f"ls -lah {param.save_loc}/{output_filename}")
