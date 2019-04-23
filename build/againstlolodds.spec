# -*- mode: python -*-
from kivy.deps import sdl2, glew
block_cipher = None


a = Analysis(['..\\againstlolodds\\main.py'],
             pathex=['C:\\Users\\Noah\\Documents\\projects\\againstlolodds\\bin'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [('againstlolodds.kv', '../againstlolodds/againstlolodds.kv', 'DATA')]

exe = EXE(pyz, Tree('../res', 'res'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in sdl2.dep_bins + glew.dep_bins],
          name='againstlolodds',
          debug=False,
          strip=False,
          upx=True,
          console=False )
