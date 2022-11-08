import click
import os
import typing
from InterfaceCreator import InterfaceCreator

@click.command()    
@click.argument('source', type=click.Path(), required=True)
@click.argument('dest', type=click.Path(), required=True)
@click.option('--cwd', type=click.Path(), default=os.getcwd(), help='The current working directory')
@click.option('--ignoredec', help="ignore all decorators", is_flag=True)
@click.option('--enforcedec', '-ed', type=click.STRING, default=["cached_property"], multiple=True, help="enforce decorators")
@click.option('--nformat', help="dont format the source code", is_flag=True)
@click.option('--nskiplocal', help="not skipping local imports", is_flag=True)
def create_interface(source, dest, cwd, ignoredec, enforcedec : typing.List[str], nformat, nskiplocal):
    """
    creates an interface from a source string
    """
    if cwd != os.getcwd():
        os.chdir(cwd)
    
    # check if source exists
    if not os.path.exists(source):
        click.echo(f"source file {source} does not exist")
        return
    
    # test if autopep8 is installed
    try:
        import autopep8
    except ImportError:
        if not nformat:
            click.echo("autopep8 is not installed, will not format the source code")
        nformat = True
    
    # create the interface
    InterfaceCreator.createInterface(
        source, 
        dest, 
        ignoreDecorator=ignoredec, 
        enforcedDecorators=enforcedec, 
        formatSource=not nformat,
        skipLocalImports=not nskiplocal
    )
    
if __name__ == "__main__":
    create_interface()