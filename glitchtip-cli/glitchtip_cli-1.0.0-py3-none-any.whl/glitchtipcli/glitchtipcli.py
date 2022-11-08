import os
import re
import sys
from typing import Dict, Any
from rich.progress import track
from dotenv import load_dotenv
import pyfiglet
from tabulate import tabulate
from yaspin import yaspin
import emoji
import click
import requests
import time
import json
from rich import print
# from rich.console import Console
# from rich.markdown import Markdown
from rich.traceback import install

# working with a framework (click, django etc), you may only be interested
# in seeing the code from your own application within the traceback.

install(suppress=[click])


__author__ = "Mark Freer CS-SRE"


DOTENV_FILE = '.env'


def create_dotenv() -> None:
    api_key = input('GlitchTip project API key: ')
    url = input('GlitchTip instance url (https://glitchtip.example.net): ')
    # TODO: verify validity of input
    with open(DOTENV_FILE, 'w') as dotenv:
        dotenv.write(f'PROJECT_API_KEY=\'{api_key}\'\n')
        dotenv.write(f'GT_URL=\'{url}\'\n')
    print(f'Config successfully written to `.env` file.')


# loading the env file
if not os.path.isfile(DOTENV_FILE):
    print('Looks like you don\'t have a `.env` file set up yet. Let\'s do it!')
    create_dotenv()
load_dotenv()

PROJECT_API_KEY = os.getenv("PROJECT_API_KEY")
GT_URL = os.getenv("GT_URL")


def is_plain(ctx):
    return ctx.obj.get('PLAIN')


def create_dotenv():
    api_key = input('GlitchTip project API key: ')
    url = input('GlitchTip instance url (https://glitchtip.example.net): ')
    # TODO: verify validity of input

    with open('.env', 'w') as dotenv:
        dotenv.write(f'PROJECT_API_KEY=\'{api_key}\'\nGT_URL=\'{url}\'\n')
    print(f'Config successfully written to `.env` file.')

    update_gitignore = input('Do you want to add `.env` to your `.gitignore` file? (y/n): ')
    if update_gitignore != 'y':
        return
    with open('.gitignore', 'a') as gitignore:
        gitignore.write('\n# GT env config file\n.env\n')
    print('`.gitignore` file successfully updated.\n')


# loading the env file
if not os.path.isfile('.env'):
    print('\nLooks like you don\'t have a `.env` file set up yet. Let\'s do it!')
    create_dotenv()
load_dotenv()

PROJECT_API_KEY = os.getenv("PROJECT_API_KEY")
GT_URL = os.getenv("GT_URL")


@click.group()
@click.option("-p", "--plain", is_flag=True)
@click.pass_context
def main(ctx, plain) -> None:
    """
    A Glitch-tip Command line tool to query the Glitch-tip Error tracking software API.
    """

    ctx.ensure_object(dict)
    ctx.obj['PLAIN'] = plain

    if not plain:
        # Load ASCII art for terminal
        result = pyfiglet.figlet_format("Glitchtip", font="slant", width=100)
        print(result)

        # Markdown doc generations for Glitchtip
        # console = Console()
        # with open('docs/Banner.md') as md:
        #    markdown = Markdown(md.read())
        #    console.print(markdown)

        # Create a photoimage object of the image in the path
        # my_art = ascii_magic.from_image_file('images/glitchtip.png', columns=45)
        # ascii_magic.to_terminal(my_art)

        print(
            "GT, [bold blue]Open Source Error Tracking Software[/bold blue]!",
            ":coffee:",
            "[u]By[/u]",
            "[i]Mark Freer[/i]")


# ======================== The Utilities section ==============================


def print_req_fail(status_code: int) -> None:
    print(f"[red]Request failed with status code: {status_code}[/red]", file=sys.stderr)


def print_req_succ() -> None:
    print(
        emoji.emojize(
            "[green]The request was successful![/green] :rocket:"
        )
    )


def list_helper(url: str, plain: bool) -> None:
    my_headers = {"Authorization": "Bearer " + PROJECT_API_KEY}

    if plain:
        response = requests.get(url, headers=my_headers)
        if response.status_code == 200:
            click.echo(response.json())
        else:
            print_req_fail(response.status_code)
        return

    with yaspin(text="Loading data from Glitchtip", color="yellow") as spinner:
        response = requests.get(url, headers=my_headers)

    if response.status_code != 200:
        spinner.fail("\u2638 ")
        print_req_fail(response.status_code)
        return

    spinner.ok("✅ ")
    print(tabulate(response.json(), headers="keys", tablefmt="fancy_grid"))
    print_req_succ()


def create_helper(url: str, payload: Dict[str, Any], plain: bool) -> None:
    my_headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + PROJECT_API_KEY,
    }

    if plain:
        response = requests.post(url, headers=my_headers, json=payload)
        if response.status_code == 201:
            click.echo(response.json())
        else:
            print_req_fail(response.status_code)
        return

    with yaspin(text="Sending data to Glitchtip", color="yellow") as spinner:
        response = requests.post(url, headers=my_headers, json=payload)

    if response.status_code != 201:
        spinner.fail("\u2638 ")
        print_req_fail(response.status_code)
        return

    spinner.ok("✅ ")
    print(
        tabulate(
            [response.json()],
            headers="keys",
            tablefmt="fancy_grid",
        )
    )
    print_req_succ()


def delete_helper(url: str, plain: bool):
    my_headers = {
        'Accept': 'application/json',
        "content-type": "application/json",
        "Authorization": "Bearer " + PROJECT_API_KEY,
    }

    if plain:
        response = requests.delete(url, headers=my_headers)
        if response.status_code != 204:
            print_req_fail(response.status_code)
        return

    with yaspin(text="Sending data to Glitchtip", color="yellow") as spinner:
        response = requests.delete(url, headers=my_headers)

    if response.status_code != 204:
        spinner.fail("\u2638 ")
        print_req_fail(response.status_code)
        return

    spinner.ok("✅ ")
    print_req_succ()


# ======================= The Organization Section ============================


@main.group()
def org():
    """This is a command group for organization commands"""


@org.command()
@click.pass_context
def list(ctx):
    """Print the list of glitchtip organizations"""

    url_format = GT_URL + "/api/0/organizations/"
    list_helper(url_format, is_plain(ctx))


@org.command()
@click.pass_context
@click.option("-o", "--org-slug", prompt=True)
def members(ctx, org_slug):
    """Print the list of a glitchtip organization's members"""

    url_format = f"{GT_URL}/api/0/organizations/{org_slug}/members/"
    list_helper(url_format, is_plain(ctx))


@org.command()
@click.pass_context
@click.option("-n", "--name", prompt="Org name")
def create(ctx, name):
    """Create a new glitchtip organization"""

    if not name or len(name) > 200:
        print("Invalid organization name ([1..200] chars)", file=sys.stderr)
        return

    url_format = GT_URL + "/api/0/organizations/"
    payload = {"name": name}
    create_helper(url_format, payload, is_plain(ctx))


@org.command()
@click.pass_context
@click.option("-o", "--org-slug", prompt=True)
def delete(ctx, org_slug):
    """Delete a glitchtip organization"""

    url_format = f'{GT_URL}/api/0/organizations/{org_slug}/'
    delete_helper(url_format, is_plain(ctx))


# ========================== The Project Section ==============================


@main.group()
def project():
    """This is a command group for project commands"""


@project.command()
@click.pass_context
def list(ctx):
    """Print the list of glitchtip projects"""

    url_format = GT_URL + "/api/0/projects/"
    list_helper(url_format, is_plain(ctx))


@project.command()
@click.pass_context
@click.option("-n", "--name", prompt="Project name")
@click.option("-o", "--org-slug", prompt=True)
@click.option("-t", "--team-name", prompt=True)
@click.option("-p", "--platform", default="")
def create(ctx, name, org_slug, team_name, platform):
    """Create a new glitchtip project"""

    if not name or len(name) > 64:
        print("Invalid project name ([1..64] chars)", file=sys.stderr)
        return
    if len(platform) > 64:
        print("Invalid platform ([0..64] chars)", file=sys.stderr)
        return

    # GlitchTip API documentation is wrong here -> trust Mark!
    url_format = GT_URL + f"/api/0/teams/{org_slug}/{team_name}/projects/"
    payload = {
        "name": name,
        "platform": platform
    }
    create_helper(url_format, payload, is_plain(ctx))


@project.command()
@click.pass_context
@click.option("-o", "--org-slug", prompt=True)
@click.option("-p", "--project-slug", prompt=True)
def delete(ctx, org_slug, project_slug):
    """Delete a glitchtip project"""

    # GlitchTip API documentation is wrong here -> trust Mark!
    url_format = GT_URL + f'/api/0/organizations/{org_slug}/projects/{project_slug}/'
    delete_helper(url_format, is_plain(ctx))


# ============================= The Team Section ==============================


@main.group()
def team():
    """This is a command group for team commands"""


@team.command()
@click.pass_context
@click.option("-o", "--org-slug")
def list(ctx, org_slug):
    """Print the list of glitchtip teams"""

    if org_slug:
        url_format = GT_URL + f"/api/0/organizations/{org_slug}/teams/"
    else:
        url_format = GT_URL + "/api/0/teams/"
    list_helper(url_format, is_plain(ctx))


@team.command()
@click.pass_context
@click.option("-n", "--name", prompt="Team name")
@click.option("-o", "--org-slug", prompt=True)
def create(ctx, name, org_slug):
    """Create a new Team in glitchtip under your organizations ID"""

    if not name or len(name) > 50:
        print("Invalid team name ([1..50] chars)", file=sys.stderr)
        return

    url_format = GT_URL + f"/api/0/organizations/{org_slug}/teams/"
    payload = {"slug": name}
    create_helper(url_format, payload, is_plain(ctx))


@team.command()
@click.pass_context
@click.option("-n", "--name", prompt="Team name")
@click.option("-o", "--org-slug", prompt=True)
def delete(ctx, name, org_slug):
    """Delete a glitchtip team"""

    url_format = GT_URL + f'/api/0/teams/{org_slug}/{name}/'
    delete_helper(url_format, is_plain(ctx))


@team.command()
@click.pass_context
@click.option("-t", "--team-name", prompt=True)
@click.option("-o", "--org-slug", prompt=True)
def members(ctx, team_name, org_slug):
    """Print the list of a glitchtip team's members"""

    url_format = GT_URL + f'/api/0/teams/{org_slug}/{team_name}/members/'
    list_helper(url_format, is_plain(ctx))


# ============================= The Issue Section =============================


@main.group()
def issue():
    """This is a command group for issue commands"""


@issue.command()
@click.pass_context
@click.option("-o", "--org-slug", prompt=True)
def list(ctx, org_slug):
    """Print the list of glitchtip issues in an organization"""

    url_format = GT_URL + f"/api/0/organizations/{org_slug}/issues/"
    list_helper(url_format, is_plain(ctx))


def get_issue(issue_id):
    url_format = GT_URL + f"/api/0/issues/{issue_id}/"
    my_headers = {"Authorization": "Bearer " + PROJECT_API_KEY}

    response = requests.get(url_format, headers=my_headers)

    if response.status_code != 200:
        print_req_fail(response.status_code)
        return None
    return response.json()


def get_jira_info():
    jira_pat = os.getenv("JIRA_PAT")
    jira_url = os.getenv("JIRA_URL")

    if jira_pat is not None and jira_url is not None:
        return jira_pat, jira_url

    jira_pat = input('JIRA Personal Access Token: ')
    jira_url = input('JIRA instance url (https://issues.example.com): ')
    if input("Do you want to update your `.env` file with the JIRA info?[y/N] ") == 'y':
        with open(DOTENV_FILE, 'a') as dotenv:
            dotenv.write(f'JIRA_PAT=\'{jira_pat}\'\n')
            dotenv.write(f'JIRA_URL=\'{jira_url}\'\n')
        print(f'`.env` file successfully updated.')
    return jira_pat, jira_url


@issue.command()
@click.pass_context
@click.option("-i", "--issue-id", prompt=True)
@click.option("-j", "--jira-project-key", prompt=True)
def export_jira(ctx, issue_id, jira_project_key):
    """Export a glitchtip issue to JIRA"""

    jira_pat, jira_url = get_jira_info()

    issue_json = get_issue(issue_id)
    if issue_json is None:
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jira_pat}",
    }

    data = {
        "fields": {
            "project": {
                "key": jira_project_key
            },
            "summary": issue_json['title'],
            "issuetype": {
                "name": "Bug"
            },
            "description": f"Json exported from GlitchTip:\n{json.dumps(issue_json, indent=2)}",
        }
    }

    if is_plain(ctx):
        response = requests.post(
            f"{jira_url}/rest/api/2/issue/",
            headers=headers,
            data=json.dumps(data)
        )
        if response.status_code == 201:
            click.echo(response.json())
        else:
            print_req_fail(response.status_code)
        return

    with yaspin(text="Sending data to JIRA", color="yellow") as spinner:
        response = requests.post(
            f"{jira_url}/rest/api/2/issue/",
            headers=headers,
            data=json.dumps(data)
        )

    if response.status_code != 201:
        spinner.fail("\u2638 ")
        print_req_fail(response.status_code)
        return

    spinner.ok("✅ ")
    print(
        tabulate(
            [response.json()],
            headers="keys",
            tablefmt="fancy_grid",
        )
    )
    print_req_succ()


# ================== This is the User listing Section ===========


# @main.command()
# @click.argument("users")
# def list_users(users):
#     """This returns the list of glitchtip specific org users"""
#
#     url_format = GT_URL + "/api/0/users/"
#     users = "+".join(users.split())
#
#     users_params = {"u": users}
#
#     my_headers = {"Authorization": "Bearer " + PROJECT_API_KEY}
#     response = requests.get(
#         url_format,
#         headers=my_headers,
#         params=users_params)
#
#     for i in track(range(10), description="Processing data from glitchtip..."):
#         time.sleep(0.1)  # Simulate work being done
#
#     print(tabulate(response.json(), headers="keys", tablefmt="fancy_grid"))
#     print(
#         emoji.emojize(
#             "The request was a successful, Here is your Glitchtip Users list \
#             for your organizations! :rocket:"
#         )
#     )


## ================ EMAIL Validation Section ========================================= ##

def validate_email(ctx, param, value):
    if not re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            value):
        raise click.UsageError('Incorrect email address given')
    else:
        return value

## ============================== Create user section ================================ ##


# Create superuser in Glitchtip options

# @main.command()
# @click.option('--name', prompt='Your name please')
# @click.option('--email', prompt='Your email please', callback=validate_email)
# @click.option('--org_id', prompt='Your organization ID please')
# def create_user(name, email, org_id):
#     """Creates a new glitchtip User associated with an organization"""
#
#     # API DOCs url endpoint https://app.glitchtip.com/api/0/users/
#     # or https://app.glitchtip.com/api/0/organizations/{organization_slug}/users/{id}/teams/{members_team_slug}/
#     # https://app.glitchtip.com/api/0/organizations/{organization_slug}/members/{id}/
#     # 'https://glitchtip.stage.devshift.net/api/0/organizations/cssre-admins/members/'+org_id
#
#     # Not sure what the backend api call is here more investigations is needed
#     # and perhaps an upstream changes.
#     url_format = GT_URL + '/api/0/users/'
#
#     name = "+".join(name.split())
#     email = "+".join(email.split())
#     org_id = str(org_id)
#
#     query_params = {
#         "isSuperuser": False,
#         "emails": [{'email': email}],
#         "id": org_id,
#         "isActive": True,
#         "hasPasswordAuth": False,
#         "name": name,
#         "email": email
#     }
#
#     my_headers = {
#         "content-type": "application/json",
#         "Authorization": "Bearer " + PROJECT_API_KEY,
#     }
#     response = requests.post(url_format, headers=my_headers, data=query_params)
#
#     if response.status_code == 200:
#         print("The request was a success!")
#         print(response.json())
#         print(
#             tabulate(
#                 response.data(),
#                 headers="firstrow",
#                 tablefmt="fancy_grid",
#                 showindex="always",
#             )
#         )
#         print(
#             emoji.emojize(
#                 "The request was a successful you created a new project! :rocket:"
#             )
#         )
#
#     # Code here will only not successful and return http 400 response
#     elif response.status_code == 400:
#         print("Result not found!, no user was created")


##---------------- Get the List of API token active ---------------- ###

# @main.command()
# @click.option('--token', prompt='Your provide your token ID')
# def list_tokens(token_id):
#     """Get the list of Glitchtip API tokens"""
#
#     # API Documentation https://app.glitchtip.com/api/0/api-tokens/{id}/
#
#     url_format = GT_URL + '/api/0/api-tokens/' + token_id
#     token_id = "+".join(token_id.split())
#
#     query_params = {
#         "scopes": "org:read",
#         "label": "cssre-new",
#         "token": "",
#         "id": token_id}
#
#     my_headers = {
#         "content-type": "application/json",
#         "Authorization": "Bearer " + PROJECT_API_KEY,
#     }
#     response = requests.get(url_format, headers=my_headers, json=query_params)
#
#     if response.status_code == 200:
#         for i in track(
#                 range(20),
#                 description="Processing  API token data from glitchtip..."):
#             time.sleep(0.5)  # Simulate work being done
#
#         print("The request was a success!")
#         print(
#             tabulate(
#                 response.json(),
#                 headers="firstrow",
#                 tablefmt="fancy_grid",
#                 showindex="always",
#             )
#         )
#         print(
#             emoji.emojize(
#                 "The request was a successful, here is the list of API tokens and there ID's ! :rocket:"
#             )
#         )
#
#     # Code here will only run if the request is successful
#     elif response.status_code == 400:
#         print("Result not found!, no API Token was found")
#
#     # Code here will react to failed requests


if __name__ == "__main__":
    main()
