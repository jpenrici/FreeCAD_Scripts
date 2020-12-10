# -*- Mode: Python; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-

import os
import sys

# Local
FULL_PATH = os.path.realpath(__file__)
PATH, FILENAME = os.path.split(FULL_PATH)
TOOLS = PATH + "/Tools"
sys.path.append(TOOLS)

try:
    from freecad_tools import *
except ImportError as err:
    print("Error: " + str(err))
    exit(0)

# Principal
DOC = FreeCAD.activeDocument()
DOC_NAME = "example_cube"

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
obj = cube(DOC, "cube", 5, 5, 10, 10, 10)
createDrawingPage(DOC, "cube", "Templates/A4_Landscape.svg")

# Salvar FreeCAD
saveFreeCAD(DOC_NAME, "Output")

# Salvar SVG
saveViewSVG(DOC, "Output")

# Informe final
print("Finished!")
