import typer

from neosctl import constant
from neosctl import schema
from neosctl.util import get_user_profile_section
from neosctl.util import prettify_json
from neosctl.util import remove_config
from neosctl.util import send_output
from neosctl.util import upsert_config


app = typer.Typer()


@app.command()
def init(
    ctx: typer.Context,
):
    typer.echo("Initialising [{}] profile.".format(ctx.obj.profile_name))
    gateway_api_url = typer.prompt(
        "Gateway API url",
        default=ctx.obj.get_gateway_api_url(),
    )
    registry_api_url = typer.prompt(
        "Registry API url",
        default=ctx.obj.get_registry_api_url(),
    )
    iam_api_url = typer.prompt(
        "IAM API url",
        default=ctx.obj.get_iam_api_url(),
    )
    kwargs = {}
    if ctx.obj.profile:
        kwargs["default"] = ctx.obj.profile.user
    user = typer.prompt(
        "Username",
        **kwargs,
    )
    kwargs["default"] = constant.AuthFlow.keycloak.value
    if ctx.obj.profile:
        kwargs["default"] = ctx.obj.profile.auth_flow
    auth_flow = typer.prompt("Auth flow", **kwargs)
    auth_flow = constant.AuthFlow(auth_flow)

    profile = schema.Profile(
        gateway_api_url=gateway_api_url,
        registry_api_url=registry_api_url,
        iam_api_url=iam_api_url,
        user=user,
        access_token="",
        refresh_token="",
        auth_flow=auth_flow,
    )

    upsert_config(ctx, profile)


@app.command()
def delete(
    ctx: typer.Context,
):
    typer.confirm("Remove [{}] profile".format(ctx.obj.profile_name), abort=True)
    remove_config(ctx)


@app.command()
def view(
    ctx: typer.Context,
):
    send_output(
        msg=prettify_json({**get_user_profile_section(ctx.obj.config, ctx.obj.profile_name)}),
    )
