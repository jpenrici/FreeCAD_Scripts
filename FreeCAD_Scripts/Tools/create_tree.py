# -*- Mode: Python; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-

'''
   Build a FreeCAD object from a small tree.
'''

import os
import sys
from random import randint

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
trunkName = "Trunk"
branchName = "Branch"
leafName = "Leaf"
leafsName = "Leafs"


def id(firstName, lastName=""):

    global index
    index = index + 1

    if lastName == "":
        return firstName + "_" + str(index)

    return firstName + "_" + lastName + "_" + str(index)


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
    x, y, z = (0, 0, 0)
    tree = document.addObject("App::DocumentObjectGroup", id(treeName))
    leafs = document.addObject("App::DocumentObjectGroup", id(treeName, leafsName))
    trunk = branch(document, id(treeName, branchName), x, y, z, stem)
    roof = [trunk]  # tronco (ramo principal, vertical e sem folhas)
    
    top = 2 * stem/3.0
    for i in range(1, branches):
        # Detalhes
        idBranch = id(treeName, branchName)
        idLeaf = id(treeName, leafName)
        fork = randint(int(top), stem)     # posição da bifurcação
        width = stem / randint(2, 5)       # tamanho do ramo
        pitch = randint(10, 85)            # giro entorno do eixo Y
        roll = randint(10, 85)             # giro entorno do eixo X
        # Ramo
        newBranch = branch(document, idBranch, x, y, z, width)
        rotate_euler(document, idBranch, 0, pitch, roll)
        move(document, idBranch, x + thickness / 2, y, fork)
        roof += [newBranch]
        # Folhas
        newLeaf = leafArea(document, idLeaf, x, y, z, 1.5)
        boundBox = newBranch.Shape.BoundBox
        move(document, idLeaf, boundBox.XMax, boundBox.YMin, boundBox.ZMax)
        leafs.addObject(newLeaf)

    if len(roof) > 1:
        union = multifuse(document, id(treeName, trunkName), roof)
    else:
        union = roof[-1]

    tree.addObject(leafs)
    tree.addObject(union)

    return tree


if __name__ == '__main__':
    # Informe
    print("PATH: " + PATH)
    print(80 * '-')

    # Exemplo de Uso
    DOC = build("simple_tree")

    # tree(document, treeName, stem, branches)
    tree_1 = createTree(DOC, "Tree01", 10, 10)

    DOC.recompute() 

    # Salvar FreeCAD
    # saveFreeCAD(DOC, PATH + "/../Output")

    # Informe final
    print("Finished!")
