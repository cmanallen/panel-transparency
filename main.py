"""Panel helper.

Manage the opacity of the Gnome-Shell panel by the current wallpaper's
color.
"""
from pydbus import SessionBus

import os
import subprocess
import time


PANEL = "Main.panel.actor"
LCORNER = "Main.panel._leftCorner.actor"
RCORNER = "Main.panel._rightCorner.actor"

VISIBLE = "black"
INVISIBLE = "rgba(0,0,0,0)"


def _set_panel_css(visible=True):
    color = VISIBLE if visible else INVISIBLE

    service = SessionBus().get("org.gnome.Shell")
    service.Eval("{}.style='background-color: {};'".format(PANEL, color))
    service.Eval(
        "{}.style='-panel-corner-background-color: {};"
        "-panel-corner-border-color: transparent;'".format(LCORNER, color))
    service.Eval(
        "{}.style='-panel-corner-background-color: {};"
        "-panel-corner-border-color: transparent;'".format(RCORNER, color))


def _get_most_frequent_color(image):
    color_list = image.getcolors(16777216)  # 256 * 256 * 256 = 16.7m
    color_item = color_list[0]
    for occurance, colors in color_list:
        if occurance > color_item[0]:
            color_item = (occurance, colors)
    return color_item[1]


def _is_bright_image(path):
    """Return the average color of the image."""
    from PIL import Image

    image = Image.open(path)
    image = image.crop((0, 0, image.size[0], image.size[1] // 50))
    print(image.size)

    red, green, blue = _get_most_frequent_color(image)
    return (0.2126 * red) + (0.7152 * green) + (0.0722 * blue) > 125


def _handle_image_path(path):
    """Verify the provied path is an image path."""
    ext = os.path.splitext(path)[1]
    if ext not in [".gif", ".jpeg", ".jpg", ".png"]:
        return None

    visible = _is_bright_image(path[7:])
    _set_panel_css(visible)


def _monitor(cmd):
    """Monitor a long lived process.

    :param cmd: Long lived command.
    """
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = p.stdout.readline()
        if line == "" and p.poll() is not None:
            break
        event, _, path = line.decode("utf-8").partition(" ")
        _handle_image_path(path.rstrip().replace("'", ""))

        # Sleep the process to give the system a break.
        time.sleep(5)


if __name__ == "__main__":
    _monitor("gsettings monitor org.gnome.desktop.background picture-uri")
