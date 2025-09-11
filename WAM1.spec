# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['WAM1.py'],
    pathex=[],
    binaries=[],
    datas=[('button.py', '.')],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='WAM1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['mole_logo.ico'],
)
app = BUNDLE(
    exe,
    name='WAM1.app',
    icon='mole_logo.ico',
    bundle_identifier=None,
)
