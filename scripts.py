import os
import sys
import subprocess as subp
from pathlib import Path


BUILD_DIR = Path('build')


def build():
    os.chdir(BUILD_DIR)
    subp.run([sys.executable, '-m' 'PyInstaller', 'againstlolodds.spec'])
