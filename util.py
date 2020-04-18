import plistlib
from pathlib import Path
import shutil
import os
import contextlib



def read_plist(path):
    with open(path, 'rb') as fd:
        return plistlib.load(fd)

def write_plist(value, path):
    with open(path, 'wb') as fd:
        plistlib.dump(value, fd)

def copytree_overwrite(src, dst):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
