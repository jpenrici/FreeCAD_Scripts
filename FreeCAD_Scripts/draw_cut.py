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

# SIMPLE CUBE DESIGN
DOC = FreeCAD.activeDocument()
DOC_NAME = "example_cut"

if DOC is None:
    FreeCAD.newDocument(DOC_NAME)
    FreeCAD.setActiveDocument(DOC_NAME)
    DOC = FreeCAD.activeDocument()
    print("New Doc: " + DOC_NAME)
else:
    print("Rebuild ...")
    removeAllObjects(DOC)
    print("Clear Doc ...")

# Objeto
# cube(document, name, x, y, z, lengthSide, widthSide, height)
c1 = cube(DOC, "c1", 0, 0, -2, 10, 20, 10)
c2 = cube(DOC, "c2", 10, 10, 2, 10, 10, 10)
c3 = cube(DOC, "c3", 0, 10, -2, 15, 20, 10)
c4 = cube(DOC, "c4", 10, 0, 2, 15, 10, 10)
f1 = fuse(DOC, "f1", c1, c3)
f2 = fuse(DOC, "f2", c2, c4)
f3 = fuse(DOC, "union", f1, f2)

# cylinder(document, name, x, y, z, centralAngle, radius, height)
cl = cylinder(DOC, "cl", 5, 5, -2, 180, 5, 15)
f4 = cut(DOC, "subtract", f3, cl)

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
