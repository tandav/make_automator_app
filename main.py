'''
creates an Automator app
with a single `Run Shell Script` action (/bin/bash)
You can pass files and folders to app
or drag-and-drop em on app
or set this app as default for some types of files
(filename will be passed as a parameter)
'''

from pathlib import Path
import plistlib
import shutil


APP_NAME    = 'MyApp'
APP         = Path(APP_NAME).with_suffix('.app')
TEMPLATE    = Path('Template.app')
BASH_SCRIPT = '/usr/local/bin/python3 /Users/tandav/Desktop/test.py "$@"'


shutil.copytree(TEMPLATE, APP)


def read_plist(path):
    with open(path, 'rb') as fd:
        return plistlib.load(fd)

def write_plist(value, path):
    with open(path, 'wb') as fd:
        plistlib.dump(value, fd)

workflow_path = 'Contents/document.wflow'
info_path     = 'Contents/Info.plist'    

workflow      = read_plist(TEMPLATE /  workflow_path)
info          = read_plist(TEMPLATE / info_path)


def rename_info(info):
    prefix, dot, _ = info['CFBundleIdentifier'].rpartition('.')
    info['CFBundleIdentifier'] = prefix + dot + APP_NAME
    info['CFBundleName'] = APP_NAME


rename_info(info)
workflow['actions'][0]['action']['ActionParameters']['COMMAND_STRING'] = BASH_SCRIPT

write_plist(info    , APP / info_path)
write_plist(workflow, APP / workflow_path)
