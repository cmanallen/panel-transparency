### Panel Transparency
Panel transparency's goal is to manage the transparency of the gnome-shell panel via the relative brightness of the current wallpaper.

### Before you install
Be warned, panel transparency will not save your current panel settings.  It will create either a opaque, black panel (the default gnome-shell panel) or a completely transparent panel.  You can *attempt* to reset your settings with `ALT` + `F2`, enter `r`, and save.

### Installing
To install this project you will need to also install three system dependencies and two pip (python package manager) dependencies.

From your package manager install: `python3`, `python-pip`, and `python-gobject` (could be listed as `python-gi`).  Once you've installed the system dependencies, you will need to install `pillow` and `pydbus` through `pip`.  You can do so by running: `pip install --user package_name`.

Finally, download and extract or clone this repository.  There are no further installation proceedures.

### Running
Change directory into `panel-transparency` and run `python3 main.py`.  You can now change your wallpaper and observe the panel become transparent or visible.  There is also some debug output you can monitor.

### Running as a service.
Todo...
