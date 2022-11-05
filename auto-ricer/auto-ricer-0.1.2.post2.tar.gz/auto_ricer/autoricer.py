import pywal
import os
import typer
from time import sleep

cli = typer.Typer(add_completion=True)


@cli.command()
def from_img(wallpaper: str):

    config_folder = f"/home/{os.getlogin()}/.config/auto-ricer"

    if not os.path.isdir(config_folder):
        install_theme()
    colors_from_img = pywal.colors.get(wallpaper)

    colors_list = list(colors_from_img["colors"].values())

    final_colors = pywal.colors.colors_to_dict(colors_list, wallpaper)
    pywal.export.every(final_colors)
    pywal.sequences.send(final_colors)

    pywal.reload.xrdb()

    os.system(f"sh /home/{os.getlogin()}/.config/bspwm/bspwmrc")
    sleep(1)
    pywal.wallpaper.set_wm_wallpaper(wallpaper)

    fix_gtk_colors()

    oomox_file_path = f"/home/{os.getlogin()}/.cache/wal/colors-oomox"
    gtk_theme_command = f"cd {config_folder}/theme_materia/materia-theme && chmod +x change_color.sh && ./change_color.sh -o auto-ricer -t /home/{os.getlogin()}/.themes {oomox_file_path}"
    os.system(gtk_theme_command)

    icons_theme_command = f"cd {config_folder}/icons_papirus && chmod +x change_color.sh && ./change_color.sh -o auto-ricer -d /home/{os.getlogin()}/.icons/auto-ricer {oomox_file_path}"
    os.system(icons_theme_command)


def fix_gtk_colors():
    oomox_colors = open(f"/home/{os.getlogin()}/.cache/wal/colors-oomox", "r").read()
    oomox_colors = oomox_colors.splitlines()
    bg_color = oomox_colors[1].strip("BG=")
    oomox_colors[9] = f"BTN_BG={bg_color}"
    oomox_colors = "\n".join(oomox_colors)

    with open(f"/home/{os.getlogin()}/.cache/wal/colors-oomox", "w") as f:
        f.write(oomox_colors)


def install_theme():
    os.system(
        f"cd /home/{os.getlogin()}/.config/auto-ricer && git clone https://github.com/AbdelrhmanNile/auto-ricer.git"
    )
    os.system(
        f"cd /home/{os.getlogin()}/.config/auto-ricer/auto-ricer && cp /gtk/. /home/{os.getlogin()}/.config/auto-ricer/"
    )
    os.system(f"rm -rf /home/{os.getlogin()}/.config/auto-ricer/auto-ricer")


if __name__ == "__main__":
    cli()
