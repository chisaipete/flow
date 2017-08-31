import sublime, sublime_plugin
import sys, os, re, math

def get_plugin_setting(param):
    setting_name = 'flow.sublime-settings'
    plugin_settings = sublime.load_settings(setting_name)
    return plugin_settings.get(param)

###custom imports
###end custom imports

###command
class flowCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.status_message("Running Flow command...")

        output_text = "Flow!"

        for cursor in self.view.sel():
            self.view.insert(edit, cursor.begin(), output_text)
###end command
