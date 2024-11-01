# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env', '.env'),
    ],
    hiddenimports=[
         'pyimod02_importers',
        'opentelemetry',
        'opentelemetry.sdk',
        'opentelemetry.semconv',
        'wmi',
        'IPython.core',
        'dotenv.ipython',
        'lxml',
        'lxml.builder',
        'lxml.html',
        'lxml.objectify',
        'lxml.sax',
        'lxml.html.diff',
        'lxml.html.html5parser',
        'lxml.html._html5builder',
        'lxml.html.clean',
        'lxml.cssselect',
        'openpyxl',
        'openpyxl.reader.excel',
    ],
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
    a.zipfiles,
    a.datas,
    [],
    name='GestorDeArchivosExcel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='Imagen/GestorDeArchivosExcel.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GestorDeArchivosExcel'
)