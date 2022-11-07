from dataclasses import dataclass


@dataclass
class TgzParam:
    src_dir: str
    save_loc: str
    outfile_name: str
    prefix_timestamp: bool
    custom_timestamp_suffix: str
