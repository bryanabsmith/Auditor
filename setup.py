# https://bitbucket.org/anthony_tuininga/cx_freeze/src/1282b6b6ee637738210113dd88c3c198d475340f/cx_Freeze/samples/wx/setup.py?at=default
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("Auditor.py", base=base)
]

setup(name="Auditor",
      version="1.0",
      description="Run audits on your Mac.",
      executables=executables
)