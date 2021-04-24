# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['../practicer/app.py'],
             pathex=['D:\\01_Projects\\14_programming\\practicer\\practicer'],
             binaries=[],
             datas=[('./../exercises/*', './exercises'), ('./../challenges/*', './challenges'),
             ('./../practicer/resources/templates', './resources/templates')],
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
          name='Practicer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='./practicer.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')
