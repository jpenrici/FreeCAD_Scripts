# -*- Mode: Python; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-

# References:
# https://wiki.freecadweb.org/Scripts
#
# Test:
# FreeCAD
# OS: Debian GNU/Linux 9.13 (stretch)
# Word size of OS: 32-bit
# Word size of FreeCAD: 32-bit
# Version: 0.16
# Build type: None
# Python version: 2.7.13
# Qt version: 4.8.7
# Coin version: 4.0.0a
# OCC version: 6.8.0.oce-0.17

import os
import sys

# Local
FULL_PATH = os.path.realpath(__file__)
PATH, FILENAME = os.path.split(FULL_PATH)
FREECADPATH = "/usr/lib/freecad/lib/"
sys.path.append(FREECADPATH)

# Dependências
try:
    import FreeCAD
    from FreeCAD import Base, Vector
except ImportError as err:
    print("Error: " + str(err))
    exit(0)

try:
    import Part
    import Draft
    import Drawing
except ImportError as err:
    print("Error: " + str(err))
    exit(0)

try:
    from export_svg import *
except ImportError as err:
    print("Error: " + str(err))
    exit(0)

# Informe inicial
print("Import ok ...")


# Métodos
def build(documentName):

    document = FreeCAD.activeDocument()
    if document is None:
        FreeCAD.newDocument(documentName)
        FreeCAD.setActiveDocument(documentName)
        document = FreeCAD.activeDocument()
        print("New Doc: " + document.Name)
    elif document.Name == documentName:
        print("Rebuild ...")
        removeAllObjects(document)
        print("Clear Doc ...")
    else:
        print("There was something wrong.")
        return None

    return document


def removeAllObjects(document):

    if len(document.Objects) < 1:
        print("Nothing to remove ...")
        return

    for obj in document.Objects:
        print("Remove: " + obj.Name)
        document.removeObject(obj.Name)

    print("Cleaning finished ... ")


def line(document, name, begin, end):

    obj = document.addObject("Part::Line", name)
    obj.X1, obj.Y1, obj.Z1 = begin
    obj.X2, obj.Y2, obj.Z2 = end
    document.recompute()
    print("Line: " + name)

    return obj


def lines(document, name, points):

    total = len(points)
    if total < 2:
        return 

    group = document.addObject("App::DocumentObjectGroup", name)
    begin = points[0]
    for i in range(1, total):
        end = points[i]
        obj = line(document, name + "_" + str(i),
             (begin[0], begin[1], begin[2]),
             (end[0], end[1], end[2]))
        group.addObject(obj)
        begin = end[:]

    return group


def cube(document, name, x, y, z, lengthSide, widthSide, height):

    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x, y, z)

    obj = document.addObject("Part::Box", name)
    obj.Length = lengthSide
    obj.Width = widthSide
    obj.Height = height
    obj.Placement = pl
    document.recompute()
    print("Cube: " + name)

    return obj


def cylinder(document, name, x, y, z, centralAngle, radius, height):

    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x, y, z)

    obj = document.addObject("Part::Cylinder", name)
    obj.Angle = centralAngle
    obj.Radius = radius
    obj.Height = height
    obj.Placement = pl
    document.recompute()
    print("Cylinder: " + name)

    return obj


def sphere(document, name, x, y, z, radius):

    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x, y, z)

    obj = document.addObject("Part::Sphere", name)
    obj.Radius = radius
    obj.Placement = pl
    document.recompute()
    print("Sphere: " + name)

    return obj


def fuse(document, name, objectOne, objectTwo):

    obj = document.addObject("Part::Fuse", name)
    obj.Base = objectOne
    obj.Tool = objectTwo
    document.recompute()
    print("Fuse: " + name)

    return obj


def cut(document, name, objectOne, objectTwo):

    obj = document.addObject("Part::Cut", name)
    obj.Base = objectOne
    obj.Tool = objectTwo
    document.recompute()
    print("Cut: " + name)

    return obj    


def createDrawingPage(document, pageName, pathTemplate):

    if not document.getObject(pageName) is None:
        document.removeObject(pageName)

    # Criar página de desenho
    obj = document.addObject("Drawing::FeaturePage", pageName)
    obj.Template = pathTemplate
    document.recompute()
    print("Page: " + pageName)

    return obj


def saveFreeCAD(document, path):

    print("Export fcstd ...")
    try:
        output = path + "/" + document.Name + ".fcstd"
        document.saveAs(output)
        print("Saved: " + output)
    except Exception as err:
        print("Sorry there was something wrong.")
        print("Error: " + str(err))


def saveViewSVG(document, path):

    ViewSVG = document.getObject("ViewIso").ViewResult

    title = document.Name
    output = path + "/" + title + ".svg"
    exportSVG(title=title, filePath=output, svg=ViewSVG)

    separator = 80 * '-'
    print(separator)
    print(ViewSVG)
    print("Saved: " + output)
    print(separator)


if __name__ == '__main__':
    # Informe
    print(sys.version)
    print(FILENAME + " file methods.")
