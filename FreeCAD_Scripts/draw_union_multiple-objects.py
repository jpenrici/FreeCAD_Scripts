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
DOC = build("example_multifuse")

# cylinder(document, name, x, y, z, centralAngle, radius, height)
c1 = cylinder(DOC, "Cylinder1", 0, 0, 0, 360, 5, 10)

# cone(document, name, x, y, z, centralAngle, radiusBase, radiusTop, height)
c2 = cone(DOC, "Cone1", 0, 0, 9.8, 360, 5, 1, 10)

# multifuse(document, name, objects)
multifuse(DOC, "Multifuse", (c1, c2)) 
DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, PATH + "/../Output")

# Informe final
print("Finished!")
