# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['sec.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [
    ('Pause.png','C:\\Users\\jackf\\Documents\\FinalYearProject\\Code\Application\\Pause.png', 'Data'),
    ('Play.png', 'C:\\Users\\jackf\\Documents\\FinalYearProject\\Code\\Application\\Play.png', 'Data'),
    ('TrainingText.csv', 'C:\\Users\\jackf\\Documents\\FinalYearProject\\Code\\Application\\TrainingText.csv', 'Data')] 

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='sec',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='sec')
