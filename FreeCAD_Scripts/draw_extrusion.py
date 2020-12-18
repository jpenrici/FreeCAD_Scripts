
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
DOC = build("example_extrusion")

# regularPolygon(document, name, x, y, z, sides, radius)
regularPolygon(DOC, "Triangle", 5, 5, 0, 3, 0.5)
regularPolygon(DOC, "Square", 7, 7, 0, 4, 1)
regularPolygon(DOC, "Pentagon", 9, 7, 0, 5, 1)
regularPolygon(DOC, "Hexagon", 11, 7, 0, 6, 1)
regularPolygon(DOC, "Octagon", 14, 7, 0, 8, 2)

extrude(DOC, "Triangle", 0.2, 0, 1)
extrude(DOC, "Square", 0, 0, 1)
extrude(DOC, "Pentagon", 0, 0, 2)
extrude(DOC, "Hexagon", 0, 0, 3)
extrude(DOC, "Octagon", 0, 0, 4)

DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, PATH + "/../Output")

# Informe final
print("Finished!")
