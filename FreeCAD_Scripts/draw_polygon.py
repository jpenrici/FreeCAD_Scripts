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

# DESENHO TESTE
DOC = build("example_polygon")

# points2polygon(document, name, points)
points2polygon(DOC, "Lines1", [(0, 2, 0), (5, 2, 0), (5, 7, 0)]) 
points2polygon(DOC, "Lines2", [(0, 2, 1), (5, 2, 1), (5, 7, 1), (0, 2, 1)])

# regularPolygon(document, name, x, y, z, sides, width)
regularPolygon(DOC, "Square1", 0, 0, 0, 4, 1)
regularPolygon(DOC, "Square2", 1, 0, 0, 4, 1)
regularPolygon(DOC, "Pentagon", 2, 0, 0, 5, 1)
regularPolygon(DOC, "Hexagon", 3, 0, 0, 6, 1)
regularPolygon(DOC, "Octagon", 5, 0, 0, 8, 2)

DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
