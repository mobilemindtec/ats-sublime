import sublime, sublime_plugin
import subprocess
import os

class AtsFormatCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    region = sublime.Region(0, self.view.size())
    content = self.view.substr(region)

    sp = self.view.file_name().split(".")
    ext = sp[len(sp)-1]

    tmp_file = "/tmp/code.%s" % ext
    with open(tmp_file, 'w') as f:
      f.write(content)

    cmd = ["atsfmt", tmp_file]

    stdout, stderr = subprocess.Popen(
      [" ".join(cmd)],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,      
      shell=True).communicate()

    if stderr.strip():
      sublime.error_message("ATS format error: %s" % stderr.strip().decode('UTF-8'))
      print("ATS FORMAT ERROR: %s" % stderr.strip().decode('UTF-8'))
    else:      
      self.view.replace(edit, region, stdout.decode('UTF-8'))

def check_is_enabled_file(file_name):    
  types = ['.dats', '.sats', '.hats']

  for t in types:
    if file_name.lower().endswith(t):
      return True
  return False

class AtsEventDump(sublime_plugin.EventListener):
      
  def on_pre_save(self, view):
    print("on_pre_save %s " % view.file_name())
    if check_is_enabled_file(view.file_name()):
      view.run_command('ats_format')


    
