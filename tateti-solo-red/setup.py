from cx_Freeze import setup, Executable
# Dependencies are automatically detected, but it might need
# fine tuning.
#buildOptions = dict(packages = ['scripts', 'pygame', 'twisted'], include_files = ['scripts/AtoZ.ttf'], excludes = [])

buildOptions = dict(packages = [], include_files = ['scripts/AtoZ.ttf'], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('menu.py', base=base, targetName = 'tateti')
]

setup(name='tateti-solo-red',
      version = '0.6',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
