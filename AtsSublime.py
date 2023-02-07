import sublime, sublime_plugin
import subprocess
import os

from Dart.sublime_plugin_lib import PluginLogger

_logger = PluginLogger(__name__)

class AtsSublimeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.insert(edit, 0, "Hello, World!")
    _logger.debug("ATS LINTER")


class AtsFormatCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    region = sublime.Region(0, self.view.size())
    content = self.view.substr(region)

    stdout, stderr = subprocess.Popen(
      ["./atsfmt", self.view.file_name()],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,      
      shell=True).communicate()

    if stderr.strip():
      print("ATS FORMAT ERROR: %s" % stderr.strip().decode())
    else:
      self.view.replace(edit, region, stdout.decode('UTF-8'))

def check_is_enabled_file(file_name):    
  types = ['.dats', '.sats', '.hats']

  for t in types:
    if file_name.lower().endswith(t):
      return True
  return False

class EventDump(sublime_plugin.EventListener):

  def __init__(self, *args, **kwargs):
    sublime_plugin.EventListener.__init__(self, *args, **kwargs)
    _logger.debug("Dartlint plugin loaded.")
      
  def on_post_save(self, view):
    if check_is_enabled_file(view.file_name()):
      view.run_command('ats_format')


    
