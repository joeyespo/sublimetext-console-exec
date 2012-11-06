# -*- coding: utf-8 -*-

"""
Console Exec

Plugin for Sublime Text 2 to execute a command and redirect its output
into a console window. This is based on the default exec command.
"""

import sublime
import sublime_plugin
import os
import sys
import subprocess
import time


class Process(object):
    def __init__(self, arg_list, env, listener,
            # "path" is an option in build systems
            path='',
            # "shell" is an options in build systems
            shell=False):

        self.listener = listener
        self.killed = False

        self.start_time = time.time()

        # Set temporary PATH to locate executable in arg_list
        if path:
            old_path = os.environ["PATH"]
            # The user decides in the build system whether he wants to append $PATH
            # or tuck it at the front: "$PATH;C:\\new\\path", "C:\\new\\path;$PATH"
            os.environ["PATH"] = os.path.expandvars(path).encode(sys.getfilesystemencoding())

        proc_env = os.environ.copy()
        proc_env.update(env)
        for k, v in proc_env.iteritems():
            proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

        self.proc = subprocess.Popen(arg_list, env=proc_env, shell=shell)

        if path:
            os.environ["PATH"] = old_path

    def kill(self):
        if not self.killed:
            self.killed = True
            self.proc.terminate()
            self.listener = None

    def poll(self):
        return self.proc.poll() == None


class ConsoleExecCommand(sublime_plugin.WindowCommand):
    def run(self, cmd=[], file_regex='', line_regex='', working_dir='', encoding='utf-8', env={}, quiet=False, kill=False, **kwargs):
        launcher = os.path.join(sublime.packages_path(), 'ConsoleExec', 'launch.exe')
        if not os.path.exists(launcher):
            if not quiet:
                print 'Error: Could not find the ConsoleExec package.'
            return
        cmd = [launcher] + map(lambda s: '"%s"' % s if ' ' in s else s, cmd)

        if kill:
            if self.proc:
                self.proc.kill()
                self.proc = None
            return

        # Default the to the current files directory if no working directory was given
        if (working_dir == '' and self.window.active_view()
                        and self.window.active_view().file_name()):
            working_dir = os.path.dirname(self.window.active_view().file_name())

        # Call get_output_panel a second time after assigning the above
        # settings, so that it'll be picked up as a result buffer
        self.window.get_output_panel("exec")

        self.encoding = encoding
        self.quiet = quiet

        self.proc = None
        if not self.quiet:
            print "Running " + " ".join(cmd)
            sublime.status_message("Building")

        merged_env = env.copy()
        if self.window.active_view():
            user_env = self.window.active_view().settings().get('build_env')
            if user_env:
                merged_env.update(user_env)

        # Change to the working dir, rather than spawning the process with it,
        # so that emitted working dir relative path names make sense
        if working_dir != '':
            os.chdir(working_dir)

        # Forward kwargs to Process
        self.proc = Process(cmd, merged_env, self, **kwargs)

    def is_enabled(self, kill=False):
        if kill:
            return hasattr(self, 'proc') and self.proc and self.proc.poll()
        else:
            return True
