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
points1 = [(0, 0, 0), (10, 0, 0), (10, 5, 0)]

# points2shape(document, name, points)
S1 = points2shape(DOC, "Shape1", points1)
DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
