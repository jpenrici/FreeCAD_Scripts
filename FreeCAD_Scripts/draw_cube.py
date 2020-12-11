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
DOC = build("example_cube")

# cube(document, name, x, y, z, lengthSide, widthSide, height)
obj_cube = cube(DOC, "cube", 5, 5, 0, 10, 10, 5)

# View
viewIso = DOC.addObject("Drawing::FeatureViewPart", "ViewIso")
viewIso.Source = DOC.getObject(obj_cube.Name)
viewIso.Direction = (1.0, 1.0, 1.0)
viewIso.X = 100.0
viewIso.Y = 150.0
viewIso.Scale = 10
viewIso.ShowHiddenLines = True

# Página de Desenho
pageViewIso = createDrawingPage(DOC, "Cube_Design", "Templates/A4_Landscape.svg")
pageViewIso.addObject(viewIso)
DOC.recompute()

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Salvar SVG
saveViewSVG(DOC, "Output")

# Informe final
print("Finished!")
