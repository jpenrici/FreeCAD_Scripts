# -*- Mode: Python; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-

# References
# https://wiki.freecadweb.org/Scripts
#
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


def removeAllObjects(document):

    if len(document.Objects) < 1:
        print("Nothing to remove ...")
        return

    for obj in document.Objects:
        print("Remove: " + obj.Name)
        document.removeObject(obj.Name)

    print("Cleaning finished ... ")


def cube(document, name, x, y, lengthSide, widthSide, height):

    obj = document.addObject("Part::Box", name)
    obj.Length = lengthSide
    obj.Width = widthSide
    obj.Height = height
    # TODO : x, y
    document.recompute()
    print("Cube: " + name)

    return obj


def cylinder(document, name, x, y, angle, radius, height):

    obj = document.addObject("Part::Cylinder", name)
    obj.Angle = angle
    obj.Radius = radius
    obj.Height = height
    # TODO : x, y
    document.recompute()
    print("Cylinder: " + name)

    return obj


def sphere(document, name, x, y, radius):

    obj = document.addObject("Part::Sphere", name)
    obj.Radius = radius
    # TODO : x, y
    document.recompute()
    print("Sphere: " + name)

    return obj


def fuseTwoObjects(document, name, objectsOne, objectsTwo):

    obj = document.addObject("Part::Fuse", name)
    obj.Base = objectsOne
    obj.Tool = objectsTwo
    document.recompute()
    print("Fuse: " + name)

    return obj


def createDrawingPage(document, objName, pathTemplate):

    if not document.getObject("Page") is None:
        document.removeObject("Page")
    document.addObject("Drawing::FeaturePage","Page")
    document.Page.Template = pathTemplate

    # Experimental
    document.addObject("Drawing::FeatureViewPart","ViewIso")
    document.ViewIso.Source = document.getObject(objName)
    document.ViewIso.Direction = (1.0,1.0,1.0)
    document.ViewIso.X = 150.0
    document.ViewIso.Y = 100.0
    document.ViewIso.Scale = 10
    #document.ViewIso.ShowHiddenLines = True
    document.Page.addObject(document.ViewIso)
    document.recompute()


def saveFreeCAD(documentName, path):

    print("Export fcstd ...")
    try:
        document = FreeCAD.activeDocument()
        print("FreeCAD.ActiveDocument: " + document.Name)
        if document.Name == documentName:
            output = path + "/" + documentName + ".fcstd"
            document.saveAs(output)
            print("Saved: " + output)
    except Exception as err:
        print("Sorry there was something wrong.")
        print("Error: " + str(err))


def saveViewSVG(document, path):

    ViewSVG = document.getObject("ViewIso").ViewResult

    title = document.Name
    output = path + "/" + title + ".svg"
    exportSVG(title=title, filePath=output , svg=ViewSVG)

    separator = 80 * '-'
    print(separator)
    print(ViewSVG)
    print("Saved: " + output)
    print(separator)

if __name__ == '__main__':
    # Informe
    print(sys.version)
    print(FILENAME + " file methods.")
