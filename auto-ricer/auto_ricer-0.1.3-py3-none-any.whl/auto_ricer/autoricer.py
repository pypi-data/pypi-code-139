import pywal
import os
import typer
from time import sleep

gh_repo = "https://github.com/AbdelrhmanNile/auto-ricer.git"

user = os.getlogin()
config_dir = f"/home/{user}/.config/auto-ricer"
bspwmrc_path = f"/home/{user}/.config/bspwm/bspwmrc"
pywal_cache_dir = f"/home/{user}/.cache/wal"

cli = typer.Typer()


@cli.command()
def from_img(wallpaper: str):

    if not os.path.isdir(config_dir):
        install_theme()

    typer.echo("Extracting colors from the wallpaper...")
    colors_from_img = pywal.colors.get(wallpaper)
    colors_list = list(colors_from_img["colors"].values())
    final_colors = pywal.colors.colors_to_dict(colors_list, wallpaper)
    pywal.export.every(final_colors)

    typer.echo("Setting color scheme...")
    pywal.sequences.send(final_colors)
    pywal.reload.xrdb()
    os.system(f"sh {bspwmrc_path} > /dev/null")
    sleep(1)

    typer.echo("Setting wallpaper...")
    pywal.wallpaper.set_wm_wallpaper(wallpaper)
    os.system(
        f"sed -i '/feh/d' {bspwmrc_path} && echo 'feh --bg-fill {wallpaper} &' >> {bspwmrc_path}"
    )

    typer.echo("Generating GTK3 theme...")
    fix_gtk_colors()
    oomox_file_path = f"{pywal_cache_dir}/colors-oomox"
    gtk_theme_command = f"cd {config_dir}/auto-ricer/gtk/theme_materia/materia-theme && chmod +x change_color.sh && ./change_color.sh -o auto-ricer -t /home/{user}/.themes {oomox_file_path} > {config_dir}/theme_log.txt"
    os.system(gtk_theme_command)

    typer.echo("Generating icons theme...")
    icons_theme_command = f"cd {config_dir}/auto-ricer/gtk/icons_papirus && chmod +x change_color.sh && ./change_color.sh -o auto-ricer -d /home/{user}/.icons/auto-ricer {oomox_file_path} > {config_dir}/icons_log.txt"
    os.system(icons_theme_command)


def fix_gtk_colors():
    oomox_colors = open(f"{pywal_cache_dir}/colors-oomox", "r").read()
    oomox_colors = oomox_colors.splitlines()
    bg_color = oomox_colors[1].strip("BG=")
    oomox_colors[9] = f"BTN_BG={bg_color}"
    oomox_colors = "\n".join(oomox_colors)

    with open(f"{pywal_cache_dir}/colors-oomox", "w") as f:
        f.write(oomox_colors)


def install_theme():

    typer.echo("Downloading gtk theme and icons theme...")
    os.system(f"mkdir {config_dir} && cd {config_dir} && git clone {gh_repo}")


if __name__ == "__main__":
    cli()
