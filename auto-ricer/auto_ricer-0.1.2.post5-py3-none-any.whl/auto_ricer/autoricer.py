import pywal
import os
import typer
from time import sleep

config_folder = f"/home/{os.getlogin()}/.config/auto-ricer"
cli = typer.Typer(add_completion=True)


@cli.command()
def from_img(wallpaper: str):

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
    gtk_theme_command = f"cd {config_folder}/auto-ricer/gtk/theme_materia/materia-theme && chmod +x change_color.sh && ./change_color.sh -o auto-ricer -t /home/{os.getlogin()}/.themes {oomox_file_path}"
    os.system(gtk_theme_command)

    icons_theme_command = f"cd {config_folder}/auto-ricer/gtk/icons_papirus && chmod +x change_color.sh && ./change_color.sh -o auto-ricer -d /home/{os.getlogin()}/.icons/auto-ricer {oomox_file_path}"
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
        f"mkdir {config_folder} && cd {config_folder} && git clone https://github.com/AbdelrhmanNile/auto-ricer.git"
    )


if __name__ == "__main__":
    cli()
