# -*- mode: python ; coding: utf-8 -*-
# https://pyinstaller.readthedocs.io/en/stable/spec-files.html

block_cipher = None
# - Script files - #
py_files = [
    '../bebarball/BeBarBall.py',
    '../bebarball/bin/GLOBAL.py',
    '../bebarball/bin/items.py',
    '../bebarball/bin/myfont.py',
    '../bebarball/bin/sound.py'
]
# - Source files - #
add_files = [
    ('../bebarball/src/font/*.ttf','src/fonts'),
    ('../bebarball/src/sound/*.wav','src/sound'),
    ('../bebarball/src/sound/*.ogg','src/sound')
]

a = Analysis(py_files, ####
             pathex=['/home/penggao/Projects/MyProject/MyGame/Pygame-Bebarball/bebarball'], ####
             binaries=None,
             datas=add_files, ####
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False
             )
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher
          )
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          exclude_binaries=True,
          name='Bebarball', ###
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, ###
          icon=''
          )

