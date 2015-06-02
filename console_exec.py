# -*- coding: utf-8 -*-

"""
Console Exec

Plugin for Sublime Text 2 to execute a command and redirect its output
into a console window. This is based on the default exec command.
"""

import os
import sys
import subprocess
import sublime
import sublime_plugin


class ConsoleExecCommand(sublime_plugin.WindowCommand):
    def run(self, cmd=[], env={}, path='', shell=False, win_console=None,
            unix_console=None, **kwargs):
        # Show message
        sublime.status_message('Running ' + ' '.join(cmd))

        # Get platform-specific command arguments
        if os.name == 'nt':
            console = win_console or ['cmd.exe', '/c']
            pause = ['&', 'pause']
            cmd = console + cmd + pause
        else:
            console = unix_console or ['xterm', '-e']
            # if a cmd list runs cmd_quote(), it's safe to do join()
            cmd = [cmd_quote(x) for x in cmd]
            pause = ['read', '-p', 'Press [Enter] to continue...']
            pause = [cmd_quote(x) for x in pause]
            cmd_bash = ['bash', '-c', ' '.join(pause)]
            cmd_bash = [cmd_quote(x) for x in cmd_bash]
            cmd_console = [' '.join(cmd), ';', ' '.join(cmd_bash)]
            cmd = console + [' '.join(cmd_console)]

        # debug
        self.debug_print('reconstructed cmd is', cmd)

        # Default the to the current file's directory if no working directory
        # was provided
        window = sublime.active_window()
        view = window.active_view() if window else None
        file_name = view.file_name() if view else None
        cwd = os.path.dirname(file_name) if file_name else os.getcwd()

        # Get environment
        env = env.copy()
        if self.window.active_view():
            user_env = self.window.active_view().settings().get('build_env')
            if user_env:
                env.update(user_env)

        # Get executing environment
        proc_env = os.environ.copy()
        proc_env.update(env)
        for key in proc_env:
            proc_env[key] = os.path.expandvars(proc_env[key])

        # Run in new console
        old_path = None
        try:
            # Set temporary PATH to locate executable in arg_list
            if path:
                old_path = os.environ['PATH']
                os.environ['PATH'] = os.path.expandvars(path)
            subprocess.Popen(cmd, env=proc_env, cwd=cwd, shell=shell)
        finally:
            if old_path:
                os.environ['PATH'] = old_path

    def debug_print (self, *arg):
        print('Console Exec:', *arg)


def cmd_quote (string):
    if sys.version_info < (3, 3):
        from pipes import quote
    else:
        from shlex import quote
    return quote(string)
