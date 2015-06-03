# -*- coding: utf-8 -*-

"""
Console Exec

Plugin for Sublime Text 2 to execute a command and redirect its output
into a console window. This is based on the default exec command.
"""

import os
import subprocess
import sublime
import sublime_plugin

try:
    from shlex import quote
except ImportError:
    from pipes import quote


class ConsoleExecCommand(sublime_plugin.WindowCommand):
    def run(self, cmd=[], env={}, path='', shell=False, win_console=None,
            unix_console=None, **kwargs):
        # Show message
        sublime.status_message('Running ' + ' '.join(cmd))

        # Get platform-specific command arguments
        if os.name == 'nt':
            console = win_console or ['cmd.exe', '/c']
            pause = ['pause']
            console_cmd = console + cmd + ['&'] + pause
        else:
            console = unix_console or ['xterm', '-e']
            escaped_cmd = ' '.join(quote(x) for x in cmd)
            pause = 'bash -c \'read -p "Press [Enter] to continue..."\''
            console_cmd = console + ['{} ; {}'.format(escaped_cmd, pause)]

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
            subprocess.Popen(console_cmd, env=proc_env, cwd=cwd, shell=shell)
        finally:
            if old_path:
                os.environ['PATH'] = old_path
