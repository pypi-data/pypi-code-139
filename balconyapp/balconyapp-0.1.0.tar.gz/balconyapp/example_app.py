from balcony import BaseBalconyApp, BalconyAWS, get_logger, get_rich_console
from typer.main import Typer
import typer
from typing import Optional
import jmespath
from typing import List, Set, Dict, Tuple, Optional, Union

_balcony = BalconyAWS()
console = get_rich_console()
logger = get_logger(__name__)


def get_iam_roles() -> List[Dict]:
    """Example function that reads from AWS using balcony"""
    iam_reader = _balcony.get_service('iam').get_service_reader()
    roles = iam_reader.read_operation('Role', 'ListRoles')
    if not roles:
        # use the balcony debugger for your 
        logger.debug("[red]Failed to read IAM Roles[/]")
        return roles
    # you can use the `rich console`, and use markups to colorize output
    console.print('[green]Roles:[/]')
    console.print(roles)
    return roles


class ExampleBalconyApplication(BaseBalconyApp,
        author="<author-name>", 
        app_name="<your-app-name>", 
        description="<descrption-of-your-app>",
        tags=('tag1', 'tag2',)
    ):
    
    def __init__(self, *args, **kwargs) -> None:
        """This method has to be available for all apps"""
        super().init(*args, **kwargs)

    def get_data(self, *args, **kwargs) -> Union[Dict, List]:
        """Implement this method to make your application usable
        on Balcony HTTP API."""
        raise NotImplementedError("Implement this method for your app \
            to be available on Balcony HTTP API.")
    
    def get_cli_app(self, *args, **kwargs) -> typer.main.Typer:
        """Create and return a Typer app. Your app will be nested 
        under the `balcony apps` command by its name.
        """
        
        app = typer.Typer(no_args_is_help=True)
        
        @app.command('your-command-name')
        def _example_command(
            argument1: Optional[str] = typer.Argument(None, show_default=False,help='argument name'),
        ):
            console.print('[bold]Hello, World from ExampleBalconyApplication.[/]')
            console.print(f'Got argument: {argument1}')
        
        return app
                
    


