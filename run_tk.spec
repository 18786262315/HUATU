# -*- mode: python -*-

block_cipher = None


a = Analysis(['run_tk.py'],
             pathex=['e:\\��������\\�ز���Ŀ\\�Զ���ͼ\\HUATU'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='run_tk',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='195.ico')
