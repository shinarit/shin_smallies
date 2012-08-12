#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import gui
from sys import argv

if __name__ == "__main__":
    # Ha meghívák
    app = gui.KamionGUI()
    if ("--nopause" in argv) or ("-np" in argv):
        app.PauseOnError(False)
    if ("--abort" in argv) or ("-a" in argv):
        app.AbortOnError(True)
    app.Run()
