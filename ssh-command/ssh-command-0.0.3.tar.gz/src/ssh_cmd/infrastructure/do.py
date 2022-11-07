from typing import Optional, Union
from pydantic import BaseModel

class CommandContextDO(BaseModel):
    connection: str='smart'
    module_path: str='/usr/local/bin/ansible'
    forks: int= 1
    timeout: int=300 
    remote_user: str='root'
    ask_pass: bool = False 
    ssh_extra_args: Optional[str] = None
    sftp_extra_args: Optional[str] = None
    scp_extra_args: Optional[str] = None 
    ask_value_pass: bool = False
    listhosts: bool = False 
    listtasks: bool = False 
    listtags: bool = False
    syntax: bool = False
    ssh_common_args='-o StrictHostKeyChecking=no'
    become: Optional[str] = None
    become_method: Optional[str] = None
    become_user: str = 'root' 
    check: bool = False 
    diff: bool = False
    verbosity: int = 1

class CommandSettingDetailDO(BaseModel):
    command: Union[str, dict]
    module: str = 'shell'
    retries: int = 2
    timeout: int = 3
    delay: float = 0.1

class CommandHostDO(BaseModel):
    ip: str
    hostname: Optional[str] = None
    port: int = 22
    username: str = 'root'

class CommandResponseDO(BaseModel):
    status: str
    ip: str
    message: Optional[str] = None
    exception: Optional[str] = None
    stdout: Optional[str] = None
    cmd: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    delta_time: Optional[str] = None
    entry_time: Optional[str] = None
    exit_time: Optional[str] = None
    stderr: Optional[str] = None