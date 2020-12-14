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
points1 = [(0, 0, 0), (10, 0, 0), (10, 5, 0)]

# ponto final redundante
points2 = [(0, 0, 1), (10, 0, 1), (10, 5, 1), (0, 0, 1)]

# points2polygon(document, name, points)
points2polygon(DOC, "Lines", points1) 
points2polygon(DOC, "Polygon", points2)

# regularPolygon(document, name, x, y, z, sides, radius)
regularPolygon(DOC, "Square", 7, 7, 2, 4, 1)
regularPolygon(DOC, "Pentagon", 9, 7, 2, 5, 1)
regularPolygon(DOC, "Hexagon", 11, 7, 2, 6, 1)
regularPolygon(DOC, "Octagon", 14, 7, 2, 8, 2)

DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
