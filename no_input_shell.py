from pathlib import Path
import shutil
import util
import os
import runpy


APPS_DIR          = Path(os.environ['DOTFILES_DIR']) / 'Services'
TEMPLATE = Path('no_input_shell.workflow')


def make_workflow(name, shell_script):
    workflow_path = 'Contents/document.wflow'
    info_path     = 'Contents/Info.plist'   

    WF = (APPS_DIR / name).with_suffix('.workflow')
    util.copytree_overwrite(TEMPLATE, WF)

    workflow      = util.read_plist(TEMPLATE /  workflow_path)
    info          = util.read_plist(TEMPLATE / info_path)

    info['NSServices'][0]['NSMenuItem']['default'] = name
    workflow['actions'][0]['action']['ActionParameters']['COMMAND_STRING'] = shell_script

    util.write_plist(info    , WF / info_path)
    util.write_plist(workflow, WF / workflow_path)
    


make_workflow('bookmark'        , '/usr/local/opt/python@3.8/bin/python3 /Users/tandav/Documents/GoogleDrive/entrypoint/projects/save_bookmark/main.py')
make_workflow('bookmark-default', '/usr/local/opt/python@3.8/bin/python3 /Users/tandav/Documents/GoogleDrive/entrypoint/projects/save_bookmark/main.py --default-folder')
make_workflow('gg'        , 'open https://github.com')
make_workflow('open iTerm', 'open -a iTerm')
# make_workflow('tmp notes' , 'open -a "Sublime Text" /Users/tandav/Documents/GoogleDrive/entrypoint/projects/tmp_notes')
make_workflow('tmp notes' , '/Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl /Users/tandav/Documents/GoogleDrive/entrypoint/projects/tmp_notes')


# update symlinks in ~/Library/Services
with util.working_directory(APPS_DIR):
    runpy.run_path('README.py') 
