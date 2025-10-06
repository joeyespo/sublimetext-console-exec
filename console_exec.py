"""
Console Exec

Plugin for Sublime Text to execute a command and redirect its output
into a console window. This is based on the default exec command.
"""

import os
import subprocess
import sys

import sublime
import sublime_plugin

try:
    from shlex import quote
except ImportError:
    from pipes import quote


class ConsoleExecCommand(sublime_plugin.WindowCommand):
    def run(
        self, cmd=[], env={}, path='', shell=False, win_console=None,
        unix_console=None, mac_console=None, **kwargs,
    ):
        # Show message
        sublime.status_message('Running ' + ' '.join(cmd))

        # Get platform-specific command arguments
        if sys.platform in ['win32', 'cygwin'] or os.name == 'nt':
            console = win_console or ['cmd.exe', '/c']
            pause = ['pause']
            console_cmd = console + cmd + ['&'] + pause
        elif sys.platform == 'darwin':
            console = mac_console or ['open', '-a', 'Terminal.app']
            escaped_cmd = ' '.join(quote(x) for x in cmd)
            inline_script = (
                f'tell application "Terminal"\n'
                f'do script "{escaped_cmd}"\n'
                f'activate\n'
                f'end tell'
            )
            console_cmd = ['osascript', '-e', inline_script]
        else:
            if sys.platform not in ['linux', 'linux2']:
                sublime.status_message((
                    f'Console Exec: Unsupported platform "{sys.platform}", '
                    f'using Linux config by default (please submit a GitHub '
                    f'issue if this is not correct)'
                ))
            console = unix_console or ['xterm', '-e']
            escaped_cmd = ' '.join(quote(x) for x in cmd)
            pause = 'bash -c \'read -p "Press [Enter] to continue..."\''
            console_cmd = console + ['{} ; {}'.format(escaped_cmd, pause)]

        # Default to current file's directory if no working directory provided
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
