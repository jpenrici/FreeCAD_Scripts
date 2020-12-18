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
DOC = build("example_cylinder")

# Grupo para conter os cilindros
group = DOC.addObject("App::DocumentObjectGroup", "Group_Cylinder")

# cylinder(document, name, x, y, z, centralAngle, radius, height)
cylinders = []
radius = 2.5
for i in range(1,6):
	angle = 360 / i
	group.addObject(cylinder(DOC, "C" + str(angle), 0, i * radius, 0, angle, radius, 5))
DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, PATH + "/../Output")

# Informe final
print("Finished!")
