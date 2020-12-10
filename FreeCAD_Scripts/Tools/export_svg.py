# -*- Mode: Python; coding: utf-8; indent-tabs-mpythoode: nil; tab-width: 4 -*-

# viewBox
VBX = 400  # largura
VBY = 400  # altura


def exportSVG(title="CAD", filePath="FreeCAD.svg", svg="<!-- SVG -->"):

    if svg is None:
        return

    print("Export svg ...")

    head = '''<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg width="#VBX#px" height="#VBY#px" viewBox="0 0 #VBX# #VBY#"
        xmlns="http://www.w3.org/2000/svg" version="1.1">
        <title>#TITLE#</title>
    '''
    head = head.replace("#VBX#", str(VBX))
    head = head.replace("#VBY#", str(VBY))
    head = head.replace("#TITLE#", title)
    output = head + svg + "\n" + "</svg>"

    try:
        f = open(filePath, "w")
        f.write(output)
        f.close()
    except Exception as err:
        print("Sorry there was something wrong.")
        print("Error: " + str(err))
        exit(0)

    print("Check " + filePath)

    return output


if __name__ == '__main__':

    # Teste
    svg = exportSVG()

    # Output
    print("-" * 80)
    print("ViewBox: " + str(VBX) + "," + str(VBY))
    print(svg)
