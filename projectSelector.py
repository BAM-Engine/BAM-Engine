"""
####################################
# BAM! Engine - projectSelector.py #
####################################
# Based off've the Godot selector screen
# Except this one has "explosive" (get it) factor

Binds with projectFinder.py that scours the relevant directory for .bam files
`.bam` files are the equivilant of .godot. Larger explanation in projectFinder.py
"""

import tkinter as tk

# Initialise a window
wn = tk.Tk()
wn.title("BAM! Engine - Project Select")
