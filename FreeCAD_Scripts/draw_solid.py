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
DOC = build("example_solid")
points = [
    (0, 0, 0),
    (0, 10, 0),
    (4, 10, 0),
    (4, 8, 0),
    (2, 8, 0),
    (2, 6, 0),
    (3, 6, 0),
    (3, 4, 0),
    (2, 4, 0),
    (2, 0, 0)
]

# points2Solid(document, name, points, height)
points2Solid(DOC, "Solid", points, 2) 

DOC.recompute() 

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
