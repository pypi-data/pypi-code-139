from balcony import BaseBalconyApp, BalconyAWS, get_rich_console, get_logger
from typer.main import Typer
import typer
import jmespath
import random
import time
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from typing import List, Set, Dict, Tuple, Optional, Union
from functools import lru_cache

_balcony = BalconyAWS()

"""
- Only one permission boundary can be set, 
    - Might want want to update the existing one in the future 


- find out the templates for generating statements (for roles and users)

- create the policy
- put the permission boundary 

"""

console = get_rich_console()
logger = get_logger(__name__)

app = typer.Typer(no_args_is_help=True)

def create_permission_boundary():

    # response = client.put_user_permissions_boundary(
    #     UserName='string',
    #     PermissionsBoundary='string'
    # )
    pass


@lru_cache(maxsize=1) # print(get_shape_name.cache_info())
def get_account_id():
    sts_reader = _balcony.get_service('sts').get_service_reader()
    response = sts_reader.read_operation('CallerIdentity', 'GetCallerIdentity')
    account_id = response[0].get('Account', False)
    return account_id

def create_policy_():
    pass


def wrap_policy(statements):
    return {
        "Version": "2012-10-17",
        "Statement": statements
        # [
        #     {
        #         "Effect": "Allow",
        #         "Action": "ec2:*",
        #         "Resource": "*"
        #     }
        # ]
    }
    
    
def _policy_creation_perm_bound(role):
    pass
def generate_permission_boundary_policy_document(role):
    
    
    
    
    
    
    
    pass

# @app.callback(invoke_without_command=True)
@app.command('role')
def _role_command(
    patterns: Optional[List[str]] = typer.Option(None, "--pattern", '-p', show_default=False, help='UNIX pattern matching for generated parameters. Should be quoted. e.g. (-p "*prod-*")'),
):
    # available_services = balcony.get_available_service_node_names()
    iam_service = _balcony.get_service('iam')

    iam_reader = iam_service.get_service_reader()
    roles = iam_reader.read_operation('Role', 'GetRole', match_patterns=patterns)
    console.print(get_account_id())
    if not roles:
        console.print("[red bold]ERROR: No Roles found.")
        raise typer.Abort()
    for role in roles:    
        role_name = role.get('RoleName')
        perm_bound = role.get('PermissionsBoundary', False)
        if perm_bound:
            perm_bound_policy_arn = perm_bound.get('PermissionsBoundaryArn')
            # has perm bound, skip for now 
            logger.debug(f"{role_name} already has PermissionsBoundary set: {perm_bound_policy_arn}. Skipping...")
            continue
        # has no perm bound
        p_doc = generate_permission_boundary_policy_document(role)
        console.print(f"{p_doc}")
        
        
        
    
class PriviledgeEscalationPreventer(BaseBalconyApp,
        author="og", 
        app_name="apply-priviledge-escalation-preventer", 
        description="",
        tags=('iam', 'priviledge-escalation', 'security')
    ):
    
    def __init__(self, *args, **kwargs) -> None:
        pass
      
    def get_data(self, *args, **kwargs) -> dict:
        balcony = BalconyAWS()
        iam_service = balcony.get_service('iam')
        return {
            'read_only_function_count':'read_only_function_count',
            'resource_nodes': 'generated_resource_nodes'
        } 
       
    def get_cli_app(self, *args, **kwargs) -> typer.main.Typer:
        return app
                
    


"""
select some roles to start with
for each role:
    create a policy for PrvEsc-PermissionBoundary, 
    put-role-permissions-boundary

+ tf like plan and apply logic


"""