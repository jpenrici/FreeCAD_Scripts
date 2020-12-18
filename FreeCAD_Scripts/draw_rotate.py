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
DOC = build("example_rotation")

# regularPolygon(document, name, x, y, z, sides, radius)
group = DOC.addObject("App::DocumentObjectGroup", "Polygons")
group.addObject(regularPolygon(DOC, "Polygon_4",  0, 0, 0, 4, 0.5))
group.addObject(regularPolygon(DOC, "Polygon_5",  5, 0, 0, 5, 0.5))
group.addObject(regularPolygon(DOC, "Polygon_6",  10, 0, 0, 6, 0.5))

regularPolygon(DOC, "Square",  0, 0, 0, 4, 0.5)
regularPolygon(DOC, "Pentagon",  5, 0, 0, 5, 0.5)
regularPolygon(DOC, "Hexagon",  10, 0, 0, 6, 0.5)

# extrude(document, shapeName, X_direction, Y_direction, Z_direction)
extrude(DOC, "Square",  0, 0, 3)
extrude(DOC, "Pentagon",  0, 0, 4)
extrude(DOC, "Hexagon",  0, 0, 5)

# rotate(document, shapeName, yaw, pitch, roll)
rotate(DOC, "Square",   0, 0, 90)
rotate(DOC, "Pentagon", 0, 45, 0)
rotate(DOC, "Hexagon",  90, 0, 0)

DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, PATH + "/../Output")

# Informe final
print("Finished!")
