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
    2. Reads from the Documents/ Folder
"""

##########
# Modules
########
from pathlib import Path as ph
import platform as pt
#import sys as sy

# Third Party
import profilesReader as pr


# Check version
os = pt.system()
release = pt.release()
version = pt.version()

openProjects = []

# Refer to Works.1
# WORK HERE
def checkControl(version):
    path = eval(pr.readProfiles("controlPath").strip())

    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    with open(path, "r") as f:
        for line in f:
            openProjects.append(line.rstrip())
    print(openProjects)

# Refer to Works.2
"""
def checkProjects(openProjects):
    path = pr.readProfiles("controlPath")
    print(type(path))
    for project in openProjects:
        with open(path, "w") as f:
            print(f)
"""

if __name__ == "__main__":
    print(f"Running: {version}")
    checkControl(os)
    #checkProjects(openProjects)
