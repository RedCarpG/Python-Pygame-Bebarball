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
    ('../bebarball/src/font/*.ttf','src/font'),
    ('../bebarball/src/sound/*.wav','src/sound'),
    ('../bebarball/src/sound/*.ogg','src/sound')
]

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
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='BeBarBall')
