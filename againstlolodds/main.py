import sys
from kivy.resources import resource_add_path
from againstlolodds.app import AgainstLoLOddsApp
from kivy.app import Builder
from pathlib import Path


def run():
    if hasattr(sys, '_MEIPASS'):
        pyinstaller_data = Path(sys._MEIPASS)
        resource_add_path(str(pyinstaller_data))
        KV = pyinstaller_data / 'againstlolodds.kv'
        Builder.load_file(str(KV))

    AgainstLoLOddsApp().run()


if __name__ == '__main__':
    run()
