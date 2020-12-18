# -*- Mode: Python; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-

import os
import sys

# Local
PATH, FILENAME = os.path.split(os.path.realpath(__file__))
sys.path.append(PATH + "/Tools")

try:
    from freecad_tools import *
except ImportError as err:
    print("Error: " + str(err))
    exit(0)

# SIMPLE DESIGN
DOC = build("example_points2shape")

# points2shape(document, name, points)
S1 = points2shape(DOC, "Shape1", [(0, 1, 0), (10, 1, 0), (10, 5, 0)])
DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, PATH + "/../Output")

# Informe final
print("Finished!")
