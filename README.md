# Python-With-Gtk-Template
A template project for Python with Gtk applications.

### Requirements
* PyGObject (Gtk introspection library)
* pygobject-stubs (For actually getting pylsp or python-language-server to auto complete in LSPs. Do if GTK3 --no-cache-dir --config-settings=config=Gtk3,Gdk3,Soup2)
* pyxdg (Desktop ".desktop" file parser)
* setproctitle (Define process title to search and kill more easily)
* sqlmodel (SQL databases and is powered by Pydantic and SQLAlchemy)

### Note
* pyrightconfig.json can prompt IDEs that use pyright lsp on where imports are located- look at venvPath and venv. "venvPath" is parent path of "venv" where "venv" is just the name of the folder under the parent path that is the python created venv.
* Move respetive sub folder content under user_config to the same places in Linux. Though, user/share/<app name> can go to ~/.config folder if prefered.
* In additiion, place the plugins folder in the same app folder you moved to /usr/share/<app name> or ~/.config/<app name> .
There are a "\<change_me\>" strings and files that need to be set according to your app's name located at:
* \_\_builtins\_\_.py
* user_config/bin/app_name
* user_config/usr/share/app_name
* user_config/usr/share/app_name/icons/app_name.png
* user_config/usr/share/app_name/icons/app_name-64x64.png
* user_config/usr/share/applications/app_name.desktop


For the user_config, after changing names and files, copy all content to their respective destinations.
The logic follows Debian Dpkg packaging and its placement logic.
