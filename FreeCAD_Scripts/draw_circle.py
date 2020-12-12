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
DOC = build("example_lines")
d = 20  # Dimension

# ellipse(document, name, x, y, z, majorRadius, minorRadius, startAngle, endAngle)
ellipse(DOC, "Ellipse", 0, 0, 0, 5, 10, 0, 359)

# circle(document, name, x, y, z, radius)
circle(DOC, "Circle", 10, 10, 0, 5)

# arc(document, name, x, y, z, radius, startAngle, endAngle)
arc(DOC, "Arc", 15, 15, 0, 10, 0, 180)

DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
