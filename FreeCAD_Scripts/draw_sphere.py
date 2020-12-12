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
DOC = build("example_sphere")

# sphere(document, name, x, y, z, radius)
sphere(DOC, "s1", 0, 0, -10, 10)
sphere(DOC, "s2", 10, 10, 10, 10)
sphere(DOC, "s3", 20, 20, 0, 10)
sphere(DOC, "s4", 30, 30, 10, 10)
DOC.recompute() 

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
