"""
##################################
# BAM! Engine - projectFinder.py #
##################################
# The backend of {insert file name}
# Backend (finding files, etc) of projectSelector.py

Works:
    1. When the program is first initialised, it checks if `control.txt` is existing in the
        specified file location (defaulting to the `Documents/` directory of your system).
        If that file cannot be found, it creates a new folder that is called `BAM` in the
        `Documents/` directory, along with the `control.txt` file.
"""

##########
# Modules
########
from pathlib import Path as ph
import platform as pt
import sys as sy

# Check version
# For file creation means
# linux: ~/Documents/BAM
# Windows: C:/Users/{user}/Documents/BAM - May need to include OneDrive idk I don't use Microslop
version = pt.system()
release = pt.release()
# Version is (may?) be irrelevant

openProjects = []

# Refer to Works.1
def checkControl(version):
    with open(ph.home() / "Documents" / "BAMEngine" / "control.txt", "r") as f:
        contents = f.read()
        print(contents)
        openProjects.append(f.readlines())
        print(openProjects)

if __name__ == "__main__":
    print(f"Running: {version}")
    checkControl(version)
