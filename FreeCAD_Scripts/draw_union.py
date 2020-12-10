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
DOC_NAME = "example_union"

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
# sphere(document, name, x, y, z, radius)
s1 = sphere(DOC, "s1", 0, 0, -2, 10)
s2 = sphere(DOC, "s2", 10, 10, 2, 10)
s3 = sphere(DOC, "s3", 0, 10, -2, 10)
s4 = sphere(DOC, "s4", 10, 0, 2, 10)
f1 = fuse(DOC, "f1", s1, s2)
f2 = fuse(DOC, "f2", s3, s4)
f3 = fuse(DOC, "union", f1, f2)

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
