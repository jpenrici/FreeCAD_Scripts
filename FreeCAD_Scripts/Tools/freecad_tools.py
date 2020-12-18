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
from math import pi, sin, cos

# Local
FULL_PATH = os.path.realpath(__file__)
PATH, FILENAME = os.path.split(FULL_PATH)
FREECADPATH = "/usr/lib/freecad/lib/"
sys.path.append(FREECADPATH)
sys.path.append(PATH)


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
    """
    :param documentName: string
    :return FreeCAD.activeDocument()
    """

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
        print("This script provides for the use of only the active document.")
        exit(0)

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
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object
    :param begin: tuple of numbers, initial coordinate (x1, y1, z1)
    :param end: tuple of numbers, final coordinate (x2, y2, z2)
    :return Part::Line
    """

    obj = document.addObject("Part::Line", name)
    obj.X1, obj.Y1, obj.Z1 = begin
    obj.X2, obj.Y2, obj.Z2 = end
    document.recompute()
    print("Line: "  + obj.Name)

    return obj


def lines(document, name, points):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object
    :param points: tuple of numbers, coordinate list (x, y, z)
    :return Lines in App::DocumentObjectGroup
    """

    total = len(points)
    if total < 2:
        return 

    group = document.addObject("App::DocumentObjectGroup", name)
    begin = points[0]
    for i in range(1, total):
        end = points[i]
        obj = line(document, name + "_" + str(i), begin, end)
        group.addObject(obj)
        begin = end[:]
    document.recompute()

    return group


def points2polygon(document, name, points):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param points: tuple of numbers, coordinate list (x, y, z)
    :return Part::Polygon
    """

    total = len(points)
    if total < 3:
        return 

    x1, y1, z1 = points[0]
    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x1, y1, z1)

    vertex = []
    for p in points:
        vertex.append(p)
    vertex.append(points[0])

    obj = document.addObject("Part::Polygon", name)
    obj.Nodes = vertex
    obj.Placement = pl
    document.recompute()
    print("Polygon " + obj.Name + ": " + str(obj.Placement))

    return obj   


def regularPolygon(document, name, x, y, z, sides, width):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis    
    :param sides: number of sides
    :param width: side size
    :return Part::Polygon
    """

    if sides < 3:
        return

    points = [(x, y, z), (x + width, y, z)]  # Primeiro lado
    angle = 360 / sides                      # Ângulo interno
    for i in range(2, sides):
        x1, y1, z1 = points[-1]              # Último ponto
        rad = angle * pi / 180               # Ângulo em radianos
        points += [(x1 + width * cos(rad), y1 + width * sin(rad), z)]
        angle += 360 / sides

    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x, y, z)

    obj = points2polygon(document, name, points)
    obj.Placement = pl
    document.recompute()
    print("Regular Polygon " + obj.Name + ": " + str(obj.Placement))

    return obj


def ellipse(document, name, x, y, z, majorRadius, minorRadius, startAngle, endAngle):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param majorRadius: number
    :param minorRadius: number
    :param startAngle: number
    :param endAngle: number
    :return Part::Ellipse
    """

    if startAngle == endAngle:
        startAngle = 0.0

    if startAngle > endAngle:
        angle = startAngle
        startAngle = endAngle
        endAngle = angle

    if minorRadius > majorRadius:
        radius = majorRadius
        majorRadius = minorRadius
        minorRadius = radius

    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x, y, z)

    obj = document.addObject("Part::Ellipse", name)
    obj.Angle0 = startAngle
    obj.Angle1 = endAngle
    obj.MajorRadius = majorRadius
    obj.MinorRadius = minorRadius
    obj.Placement = pl
    document.recompute()
    print("Ellipse " + obj.Name + ": " + str(obj.Placement))
    
    return obj    


def circle(document, name, x, y, z, radius):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param Radius: number
    :return Part::Ellipse (Circle)
    """

    return ellipse(document, name, x, y, z, radius, radius, 0, 360)


def arc(document, name, x, y, z, radius, startAngle, endAngle):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param Radius: number
    :param startAngle: number
    :param endAngle: number
    :return Part::Ellipse (Arc)
    """

    return ellipse(document, name, x, y, z, radius, radius, startAngle, endAngle)


def cube(document, name, x, y, z, lengthSide, widthSide, height):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param lengthSide: number, cube length
    :param widthSide: number, cube width
    :param height: number, cube height
    :return Part::Box
    """

    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x, y, z)

    obj = document.addObject("Part::Box", name)
    obj.Length = lengthSide
    obj.Width = widthSide
    obj.Height = height
    obj.Placement = pl
    document.recompute()
    print("Cube " + obj.Name + ": " + str(obj.Placement))

    return obj


def cone(document, name, x, y, z, centralAngle, radiusBase, radiusTop, height):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param centralAngle: number, central angle of the cylinder base
                         360, circle; angle between 1 and 359, arc; 0, line
    :param radiusBase: number, cone base radius
    :param radiusTop: number, cone top radius
    :param height: number, cone height
    :return Part::Cone
    """

    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x, y, z)

    obj = document.addObject("Part::Cone", name)
    obj.Angle = centralAngle
    obj.Radius1 = radiusBase
    obj.Radius2 = radiusTop
    obj.Height = height
    obj.Placement = pl
    document.recompute()
    print("Cone " + obj.Name + ": " + str(obj.Placement))

    return obj


def cylinder(document, name, x, y, z, centralAngle, radius, height):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param centralAngle: number, central angle of the cylinder base
                         360, circle; angle between 1 and 359, arc; 0, line
    :param radius: number, cylinder base radius
    :param height: number, cylinder height
    :return Part::Cylinder
    """

    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x, y, z)

    obj = document.addObject("Part::Cylinder", name)
    obj.Angle = centralAngle
    obj.Radius = radius
    obj.Height = height
    obj.Placement = pl
    document.recompute()
    print("Cylinder " + obj.Name + ": " + str(obj.Placement))

    return obj    


def sphere(document, name, x, y, z, radius):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param x: number, coordinate on the X axis
    :param y: number, coordinate on the Y axis
    :param z: number, coordinate on the Z axis
    :param radius: number, sphere radius
    :return Part::Sphere
    """

    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x, y, z)

    obj = document.addObject("Part::Sphere", name)
    obj.Radius = radius
    obj.Placement = pl
    document.recompute()
    print("Sphere " + obj.Name + ": " + str(obj.Placement))

    return obj


def points2shape(document, name, points):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param points: tuple of numbers, coordinate list (x, y, z)
    :return Part::Feature
    """

    total = len(points)
    if total < 3:
        return 

    x0, y0, z0 = points[0]
    pl = FreeCAD.Placement()
    pl.Base = FreeCAD.Vector(x0, y0, z0)      

    edges = []
    x1, y1, z1 = x0, y0, z0
    for i in range(1, total):
        x2, y2, z2 = points[i]
        edges += [Part.Line(Base.Vector(x1, y1, z1), Base.Vector(x2, y2, z2))]
        x1, y1, z1 = x2, y2, z2
    edges += [Part.Line(Base.Vector(x1, y1, z1), Base.Vector(x0, y0, z0))]

    obj = document.addObject("Part::Feature", name)
    obj.Shape = Part.Shape(edges)
    obj.Placement = pl
    document.recompute()
    print("Shape " + obj.Name + ": " + str(obj.Placement))

    return obj


def points2Solid(document, name, points, height):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param points: tuple of numbers, coordinate list (x, y, z)
    :param height: number, extrusion height
    :return Part::Feature
    """

    obj = points2polygon(document, name, points)
    # extrude(document, shapeName, X_direction, Y_direction, Z_direction)
    extrude(document, name, 0, 0, height)
    print("Solid " + obj.Name + ": " + str(obj.Placement))

    return obj


def fuse(document, name, objectOne, objectTwo):
    """
    Joins or merges two objects.
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference name of the resulting object
    :param objectOne: string, reference name of object one
    :param objectTwo: string, reference name of object two
    :return Part::Fuse
    """

    obj = document.addObject("Part::Fuse", name)
    obj.Base = objectOne
    obj.Tool = objectTwo
    document.recompute()
    print("Fuse " + obj.Name + ": " + str(obj.Placement))

    return obj


def multifuse(document, name, objects):
    """
    Joins or merges objects.
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference name of the resulting object
    :param objects: tuple, reference name of objects
    :return Part::MultiFuse
    """
    obj = document.addObject("Part::MultiFuse", name)
    obj.Shapes = objects
    document.recompute()
    print("MultiFuse " + obj.Name + ": " + str(obj.Placement))

    return obj


def cut(document, name, objectOne, objectTwo):
    """
    Subtract or cut two objects.
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference name of the resulting object
    :param objectOne: string, reference name of object one
    :param objectTwo: string, reference name of object two
    :return Part::Cut
    """

    obj = document.addObject("Part::Cut", name)
    obj.Base = objectOne
    obj.Tool = objectTwo
    document.recompute()
    print("Cut " + obj.Name + ": " + str(obj.Placement))

    return obj    


def extrude(document, shapeName, X_direction, Y_direction, Z_direction):
    """
    :param document: string, FreeCAD.activeDocument()
    :param shapeName: string, reference object
    :param X_direction: number
    :param Y_direction: number
    :param Z_direction: number
    :return Part::Feature
    """

    obj = document.getObject(shapeName)
    print(obj.Name + ": " + str(obj.Placement))

    face = Part.Face(Part.Wire(obj.Shape.Edges))
    obj.Shape = face.extrude(FreeCAD.Vector(X_direction, Y_direction, Z_direction))
    document.recompute()

    print("Extrude " + obj.Name + ": " + str(obj.Placement))

    return obj


def rotate(document, shapeName, yaw, pitch, roll):
    """
    :param document: string, FreeCAD.activeDocument()
    :param shapeName: string, reference object
    :param yaw: number, Euler angle, rotation about the Z axis
    :param pitch: number, Euler angle, rotation about the Y axis
    :param roll: number, Euler angle, rotation about the X axis
    :return Part::Feature
    """

    obj = document.getObject(shapeName)
    print(obj.Name + ": " + str(obj.Placement))

    pos = obj.Placement.Base
    centre = FreeCAD.Vector(0, 0, 0)
    rot = FreeCAD.Rotation(yaw, pitch, roll)
    pl = FreeCAD.Placement(pos, rot, centre)
    obj.Placement = pl
    document.recompute()

    print("Rotate" + obj.Name + ": " + str(obj.Placement))


def move(document, shapeName, x, y, z):
    """
    :param document: string, FreeCAD.activeDocument()
    :param shapeName: string, reference object
    :param x: number, move on the X axis
    :param y: number, move on the Y axis
    :param z: number, move on the Z axis
    :return Part::Feature
    """

    obj = document.getObject(shapeName)
    print(obj.Name + ": " + str(obj.Placement))

    vector = FreeCAD.Vector(x, y, z)
    Draft.move(obj, vector)
    document.recompute()

    print("Move " + obj.Name + ": " + str(obj.Placement))


def createDrawingPage(document, pageName, pathTemplate):
    """
    :param document: string, FreeCAD.activeDocument()
    :param name: string, reference object 
    :param pathTemplate: string, location of the template SVG file
    :return Drawing::FeaturePage
    """

    if not document.getObject(pageName) is None:
        document.removeObject(pageName)

    # Criar página de desenho
    obj = document.addObject("Drawing::FeaturePage", pageName)
    obj.Template = pathTemplate
    document.recompute()
    print("Page: " + pageName)

    return obj


def saveFreeCAD(document, path):
    """
    :param document: string, FreeCAD.activeDocument()
    :param path: string, location where the FreeCAD file will be saved
    """

    print("Export fcstd ...")
    try:
        output = path + "/" + document.Name + ".fcstd"
        document.saveAs(output)
        print("Saved: " + output)
    except Exception as err:
        print("Sorry there was something wrong.")
        print("Error: " + str(err))


def saveViewSVG(document, path):
    """
    :param document: string, FreeCAD.activeDocument()
    :param path: string, location where the SVG file will be saved
    """

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
    print(80 * '-')

    # Exemplo de Uso
    DOC = build("example_cube")

    # cube(document, name, x, y, z, lengthSide, widthSide, height)
    obj_cube = cube(DOC, "cube", 5, 5, 0, 10, 10, 5)

    # View
    viewIso = DOC.addObject("Drawing::FeatureViewPart", "ViewIso")
    viewIso.Source = DOC.getObject(obj_cube.Name)
    viewIso.Direction = (1.0, 1.0, 1.0)
    viewIso.X = 100.0
    viewIso.Y = 150.0
    viewIso.Scale = 10
    viewIso.ShowHiddenLines = True

    # Página de Desenho
    pageViewIso = createDrawingPage(DOC, "Cube_Design", PATH + "/../Templates/A4_Landscape.svg")
    pageViewIso.addObject(viewIso)
    DOC.recompute()

    # Salvar FreeCAD
    saveFreeCAD(DOC, PATH + "/../Output")

    # Salvar SVG
    saveViewSVG(DOC, PATH + "/../Output")

    # Informe final
    print("Finished!")
