Console Exec
============

Plugin for Sublime Text 2 to execute a command in a console window.
After the process exits, the console remains open and displays **"Press
any key to exit"** before closing.

This plugin is based on the exec command shipped with Sublime Text, and
uses the launcher that ships with [Crimson Editor](http://crimsoneditor.com)
to wait for a keypress before closing the window.

Source [on Github](http://github.com/joeyespo/sublimetext-console-exec)


Why?
----

Aside from personal preference of having an external debug window in web,
projects, certain runtime environments such as [Pyglet](http://www.pyglet.org/)
will not run properly within the integrated console window.


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

#### Manual installation (advanced)

Clone this repository into the Packages directory. To see where your Packages
directory is installed:

1. Run Sublime Text
2. Press CTRL+` to open the console
3. Enter `print sublime.packages_path()`

#### Easy installation

Use [Sublime Package Control](http://wbond.net/sublime_packages/package_control):

1. Select **Package Control: Install Package** from the command palette
2. Look for **ConsoleExec** and press enter to install it
