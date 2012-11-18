Console Exec
============

Plugin for Sublime Text 2 to execute a command in a console window.
After the process exits, the console remains open and displays **"Press
any key to exit"** before closing.

This plugin is based on the exec command shipped with Sublime Text, and
uses the launcher that ships with [Crimson Editor][cedit]
to wait for a keypress before closing the window.

![Running a Flask application screenshot][screenshot]

Source [available on Github][repo].

[screenshot]: https://raw.github.com/joeyespo/sublimetext-console-exec/master/examples/flask_application_screenshot.png
[cedit]: http://crimsoneditor.com
[repo]: http://github.com/joeyespo/sublimetext-console-exec


Why?
----

Aside from personal preference of having an external console in web projects,

- Sublime leaves your background process running when you quit
- Rebuilding a project overwrites your running process, leaking processes if you're not careful
- Certain environments such as [Pyglet][] will not run within the integrated console window

This plugin ties these loose ends in a familiar way.

[Pyglet]: http://www.pyglet.org


Usage
-----

In any **.sublime-build** file add the following line to run it in a console:

    "target": "console_exec"

For example, here's a modified **Python.sublime-build** file:

    {
        "cmd": ["python", "-u", "$file"],
        "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
        "selector": "source.python",
        "target": "console_exec"
    }


Installation
------------

With [Sublime Package Control][package_control], simply

1. Select **Package Control: Install Package** from the command palette
2. Locate **ConsoleExec** and press enter to install it

[package_control]: http://wbond.net/sublime_packages/package_control

#### Manual installation (advanced)

Clone this repository into the Packages directory.
To see where it's located enter `print sublime.packages_path()` in the console.


Notes
-----

This plugin is Windows-only for the moment.
