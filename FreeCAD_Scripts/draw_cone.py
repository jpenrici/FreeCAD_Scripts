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
DOC = build("example_cone")

# cone(document, name, x, y, z, centralAngle, radiusBase, radiusTop, height)
cone(DOC, "Cone_01", 0, 0, 0, 45, 5.0, 2.5, 2.5)
cone(DOC, "Cone_02", 0, 10, 0, 360, 5.0, 0.5, 5)
DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
