# -*- mode: python ; coding: utf-8 -*-
# https://pyinstaller.readthedocs.io/en/stable/spec-files.html

block_cipher = None
# - Script files - #
py_files = [
    '../bebarball/BeBarBall.py',
    '../bebarball/src/bbb_local.py',
    '../bebarball/src/bbb_items.py',
    '../bebarball/src/bbb_myfont.py',
    '../bebarball/src/bbb_sound.py',
    '../bebarball/src/bbb_frozen_dir.py',
    '../bebarball/src/__init__.py'
]
# - Source files - #
add_files = [
    ('../bebarball/data/font/*.ttf','data/font'),
    ('../bebarball/data/sound/*.wav','data/sound'),
    ('../bebarball/data/sound/*.ogg','data/sound'),
    ('../bebarball/data/sound/*.mp3','data/sound'),
    ('../bebarball/data/bebarball.ico','data')
]

icon_file = '../bebarball/data/Bebarball.ico'

a = Analysis(py_files,
             pathex=['.'],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='BeBarBall',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon=icon_file)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='BeBarBall')
