# -*- mode: python ; coding: utf-8 -*-
# 第一个路径是本地目录，第二个路径是应用目录。
a = Analysis(
    ['app.py'],
    pathex=['E:\\Environment\\anaconda3\\envs\\fast'],
    binaries=[('E:\\Environment\\anaconda3\\envs\\fast\\*.dll', '.')],
    datas=[
        ('./client/dist', 'client/dist'),
        ('E:/Environment/anaconda3/envs/fast/Lib/site-packages','.')
    ],
    hiddenimports=['fastapi','webview'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)