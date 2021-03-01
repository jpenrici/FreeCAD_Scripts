# -*- Mode: Python; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-

'''
   Build a FreeCAD object from a small tree.
'''

import os
import sys
from random import randint, choice

try:
	sys.path.append(os.path.split(os.path.realpath(__file__))[0])
	from freecad_tools import *
except ImportError as err:
	print("Error: " + str(err))
	exit(0)

# Informe inicial
print("create_tree module running ...")

# Configuração global
index = 0           # identificador do elemento
polygon = 6         # número de lados do tronco/ramo
thickness = 0.2     # espessura do ramo

# Rótulos
stemName = "_Stem"
trunkName = "_Trunk"
branchName = "_Branch"
leafName = "_Leaf"
leafsName = "_Leafs"


def id(firstName, lastName=""):

	global index
	index = index + 1

	if lastName == "":
		return firstName + "_" + str(index)

	return firstName + lastName + "_" + str(index)


def leaf(document, name, x, y, z, width):
	"""
	:param document: string, FreeCAD.activeDocument()
	:param name: string, reference object 
	:param x: number, coordinate on the X axis
	:param y: number, coordinate on the Y axis
	:param z: number, coordinate on the Z axis
	:param width: number, leaf length
	:return Part::Polygon (Solid)
	"""

	density = 0.05
	a = width * 1/4.0
	b = width * 3/4.0
	c = width * 1/8.0
	d = width * 3/8.0
	p = [ (x, y, z), (x + a, y + a, z), (x + b, y, z), (x + a, y - a, z),
		  (x, y, z), (x + c, y - d, z), (x, y - b, z), (x - c, y - d, z),
		  (x, y, z), (x - c, y + d, z), (x, y + b, z), (x + c, y + d, z) ]

	obj = points2polygon(document, name, p)
	extrude(document, name, 0, 0, density)

	return obj


def leafArea(document, name, x, y, z, radius):
	"""
	Sphere that simulates filling with leaves.
	:param document: string, FreeCAD.activeDocument()
	:param name: string, reference object
	:param x: number, coordinate on the X axis
	:param y: number, coordinate on the Y axis
	:param z: number, coordinate on the Z axis
	:param radius: number
	:return Part::Sphere
	"""
	
	return sphere(document, name, x, y, z, radius)


def branch(document, name, x, y, z, length):
	"""
	:param document: string, FreeCAD.activeDocument()
	:param name: string, reference object
	:param x: number, coordinate on the X axis
	:param y: number, coordinate on the Y axis
	:param z: number, coordinate on the Z axis
	:param length: number, branch length
	:return Part::Feature (Solid)
	"""

	return regularPolygon2Solid(document, name, x, y, z, polygon, thickness, length)


def createTree(document, treeName, stem, branches):
	"""
	:param document: string, FreeCAD.activeDocument()
	:param name: string, reference object
	:param x: number, coordinate on the X axis
	:param y: number, coordinate on the Y axis
	:param z: number, coordinate on the Z axis
	:param stem: number, stem size
	:param branches: number, number of branches
	:return Polygon (Solid) in App::DocumentObjectGroup
	"""

	# Árvore (tronco, ramificações e folhas)
	tree = document.addObject("App::DocumentObjectGroup", treeName)
	leafs = document.addObject("App::DocumentObjectGroup", treeName + leafsName)
	ramifications = document.addObject("App::DocumentObjectGroup", treeName + branchName)

	top = stem * 1/3
	x, y, z = (0, 0, 0)
	trunk = branch(document, treeName + stemName, x, y, z, stem)
	ramifications.addObject(branch(document, id(treeName, branchName), x, y, z + top, top))
	
	angles_Z = [ 50, 60, 75]
	angles_Y = [-75, -60, -45, -30, 15, 30, 45, 60, 75]
	angles_X = [-85, -70, -60, -45, -30, -15, 15, 30, 45, 50, 60, 70, 75, 85]

	box_X = [0, 0]
	box_Y = [0, 0]
	box_Z = [0, 0]

	# Ramos
	for i in range(1, branches):
		idBranch = id(treeName, branchName)
		newBranch = branch(document, idBranch, x, y, z, stem / randint(2, 5))
		rotate_euler(document, idBranch, 0, choice(angles_Y), choice(angles_X))
		move(document, idBranch, x + thickness / 2, y, z + stem - top)
		ramifications.addObject(newBranch)

		boundBox = newBranch.Shape.BoundBox
		if box_X[0] > boundBox.XMin: box_X[0] = int(boundBox.XMin)
		if box_X[1] < boundBox.XMax: box_X[1] = int(boundBox.XMax)
		if box_Y[0] > boundBox.YMin: box_Y[0] = int(boundBox.YMin)
		if box_Y[1] < boundBox.YMax: box_Y[1] = int(boundBox.YMax) 
		if box_Z[0] > boundBox.ZMin: box_Z[0] = int(boundBox.ZMin)
		if box_Z[1] < boundBox.ZMax: box_Z[1] = int(boundBox.ZMax)                                   

	# Folhas
	for j in range(0, 10 * branches):
		idLeaf = id(treeName, leafName)
		newLeaf = leafArea(document, idLeaf, x, y, z, 1.2)
		#newLeaf = leaf(document, idLeaf, x, y, z, 1.8)
		rotate_euler(document, idLeaf, choice(angles_Z), choice(angles_Y), choice(angles_X))
		move(document, idLeaf, x + randint(box_X[0], box_X[1]),	y + randint(box_Y[0], box_Y[1]),
			top + randint(box_Z[1] / 2, box_Z[1]))
		leafs.addObject(newLeaf)

	tree.addObject(leafs)
	tree.addObject(ramifications)
	tree.addObject(trunk)

	return tree


if __name__ == '__main__':
	# Informe
	print("PATH: " + PATH)
	print(80 * '-')

	# Exemplo de Uso
	DOC = build("simple_tree")

	# tree(document, treeName, stem, branches)
	tree_1 = createTree(DOC, "Tree01", 10, 15)

	DOC.recompute() 

	# Salvar FreeCAD
	saveFreeCAD(DOC, PATH + "/../Output")

	# Informe final
	print("Finished!")
