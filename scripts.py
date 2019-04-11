import os
import sys
import subprocess as subp
from pathlib import Path


ROOT = Path(__file__).parent
LIB: Path = ROOT / 'lib'
RIFT_EXPLORER: Path = LIB / 'rift-explorer' / 'Rift Explorer.exe'


def run_rift_explorer():
    subp.run([str(RIFT_EXPLORER)])
