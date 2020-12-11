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

# SIMPLE DESIGN
DOC = build("example_lines")
d = 20  # Dimension

# line(document, name, begin, end, color)
line(DOC, "X", begin=(0, 0, 0), end=(d, 0, 0))
line(DOC, "Y", begin=(0, 0, 0), end=(0, d, 0))
line(DOC, "z", begin=(0, 0, 0), end=(0, 0, d))

x, y, z = 0, 0, 0
points = []
for i in range(0, d, 2):
	points += [[x + d, y, z], [x - d, y, z]]
	if d % 2 == 0: y = y + 2
	if d % 3 == 0: z = z + 2
	d = d - 2
	
# lines(document, name, points)	
lines(DOC, "Lines", points) 
DOC.recompute()	

# Salvar FreeCAD
saveFreeCAD(DOC, "Output")

# Informe final
print("Finished!")
