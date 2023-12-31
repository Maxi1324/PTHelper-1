# Beispiel.spec

block_cipher = None

a = Analysis(['Gui2.py'],
             pathex=['.'],
             binaries=[],
             datas=[("FileIcon.png","."),("PkaHelper.exe","."),('Manis\\*.py', 'Manis'),('PKAHelper.py', 'PKAHelper'),('ManipulationDialog.py', 'ManipulationDialog'),('Graph.py', 'Graph')]
             # Andere Einstellungen hier...
            )

# Hinzufügen des Icons zur EXE-Konfiguration
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Gui2',
          debug=False,
          bootloader_ignore_signals=False,
          bootloader_ignore_ttls=False,
          icon='FileIcon.ico',  # Hier den Pfad zu deinem Icon angeben
          # Andere Einstellungen hier...
          )

# Weitere Konfigurationen und Einstellungen hier...

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               name="test",
               # Andere Einstellungen hier...
               strip=False,
               upx=True,
               upx_exclude=[],
               console=False,
               upx_options=[],
             )  # Füge dein eigenes Icon hinzu, falls benötigt

# Weitere Einstellungen und Konfigurationen hier...
