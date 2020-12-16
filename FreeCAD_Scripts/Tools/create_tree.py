# -*- Mode: Python; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-

'''
   Build a FreeCAD object from a small tree.
'''

import os
import sys
from random import randint


# Local
PATH, FILENAME = os.path.split(os.path.realpath(__file__))
sys.path.append(PATH)

try:
    from freecad_tools import *
except ImportError as err:
    print("Error: " + str(err))
    exit(0)

# Informe inicial
print("create_tree module running ...")

# Configuração
branchPolygon = 6
branchThickness = 0.2

def createBranch(document, name, x, y, z, width, angle=0.0, axis="X"):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param width: number, branch length
    :param angle: number, -60 <= angle <= 60
    :param axis: string, X or Y axis for horizontal rotation
    :return Polygon (Solid) in App::DocumentObjectGrou
    """

    group = document.addObject("App::DocumentObjectGroup", "Branch")

    # Ramo
    branch = regularPolygon(document, name, x, y, z, branchPolygon, branchThickness)
    angle = angle * pi / 180
    x1 = width * sin(angle)
    y1 = width * sin(angle)
    z1 = width * cos(angle)
    if axis.upper() == "Y":
        x1 = 0
    else:
        y1 = 0

    # Extrudar polígono
    extrude(document, name, x1, y1, z1)
    group.addObject(branch)

    # Teste de Folhagem simples em forma de esfera
    radius = 2
    leaf = sphere(document, axis + "_leaf" + name,  x + x1, y + y1, z + z1 + radius, radius)
    group.addObject(leaf)

    return group


def ramify(document, x, y, z, stem, branches):
    """
    :param document: string, FreeCAD.activeDocument()
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param stem: number, stem size
    :param branches: number, number of branches
    :return Polygon (Solid) in App::DocumentObjectGroup
    """

    # Ramificação
    group = document.addObject("App::DocumentObjectGroup", "Top")

    # TODO
    # branches

    # Teste com ramos
    for angle in [-60, -45, -30, -15, 15, 30, 45, 60]:
        for axis in ["X", "Y"]:
            # Ramo
            bif = stem / randint(2, 5)    # Posição da bifurcação
            width = stem / randint(1, 5)  # Tamanho do ramo
            name = ("_positive" + str(angle)).replace("positive-", "negative")
            branch = createBranch(document, axis + "_branch" + name, x, y, z + bif, width, angle, axis)
            # Inserir na Ramificação
            group.addObject(branch)

    return group


def createTree(document, name, x, y, z, stem, branches):
    """
    :param document: string, FreeCAD.activeDocument()
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param stem: number, stem size
    :param branches: number, number of branches
    :return Part::Polygon (Solid)
    """

    # Árvore
    group = document.addObject("App::DocumentObjectGroup", name)

    # Tronco da árvore, vertical
    trunk = createBranch(document, "Trunk", x, y, z, stem)
    group.addObject(trunk)

    # Ramos da copa da árvore
    top = ramify(document, x, y, z, stem, branches)
    group.addObject(top)

    return group


if __name__ == '__main__':
    # Informe
    print(sys.version)
    print(FILENAME + " file methods.")
    print(80 * '-')

    # Exemplo de Uso
    DOC = build("simple_tree")

    # createTree(document, name, x, y, z, stem, branches)
    tree_1 = createTree(DOC, "Tree_1", 0, 0, 0, 10, 3)

    DOC.recompute() 

    # Salvar FreeCAD
    # saveFreeCAD(DOC, "Output")

    # Informe final
    print("Finished!")
