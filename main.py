'''
creates an Automator app
with a single `Run Shell Script` action (/bin/bash)
You can pass files and folders to app
or drag-and-drop em on app
or set this app as default for some types of files
(filename will be passed as a parameter)

support only for oneliners, multi-line shell script should be used kinda like this:
<string>/usr/local/opt/python@3.8/bin/python3.8 -c 'import sys; print(sys.executable)' &gt; /Users/tandav/Desktop/log.txt</string>

'''

from pathlib import Path
import shutil
import util
import os
import runpy


# APPS_DIR          = Path(os.environ['DOTFILES_DIR']) / 'Services'
APPS_DIR          = Path.home() / 'Desktop'
# APP_TEMPLATE      = Path('Template.app')
# WORKFLOW_TEMPLATE = Path('template.workflow')

TEMPLATE = Path('Template.app')


workflow_path = 'Contents/document.wflow'
info_path     = 'Contents/Info.plist'   


def _helper(name, shell_script, suffix):
    APP = (APPS_DIR / name).with_suffix(suffix)
    shutil.copytree(TEMPLATE, APP)




def make_app(name, shell_script):
    APP = (APPS_DIR / name).with_suffix('.app')

    shutil.copytree(TEMPLATE, APP)
 
    workflow      = util.read_plist(TEMPLATE /  workflow_path)
    info          = util.read_plist(TEMPLATE / info_path)

    def rename_info(info):
        prefix, dot, _ = info['CFBundleIdentifier'].rpartition('.')
        info['CFBundleIdentifier'] = prefix + dot + name
        info['CFBundleName'] = name

    rename_info(info)
    workflow['actions'][0]['action']['ActionParameters']['COMMAND_STRING'] = shell_script

    util.write_plist(info    , APP / info_path)
    util.write_plist(workflow, APP / workflow_path)

# def make_workflow(name, shell_script):
#     WF = (APPS_DIR / name).with_suffix('.workflow')
    
#     shutil.copytree(WORKFLOW_TEMPLATE, WF)

#     workflow      = util.read_plist(TEMPLATE /  workflow_path)
#     info          = util.read_plist(TEMPLATE / info_path)

#     def rename_info(info):
#         info['NSServices'][0]['NSMenuItem']['default'] = name

#     rename_info(info)
#     workflow['actions'][0]['action']['ActionParameters']['COMMAND_STRING'] = shell_script

#     util.write_plist(info    , WF / info_path)
#     util.write_plist(workflow, WF / workflow_path)


make_app('template', '/usr/local/bin/python3 /Users/tandav/Desktop/test.py "$@"')
# make('MyApp', '/usr/local/bin/python3 /Users/tandav/Desktop/test.py "$@"')
# runpy.run_path(str(APPS_DIR / 'README.py'))
