# Aluminum Tab System

## Objectives

First, some background. much of the work I do centers around design, fabrication, and install of perforated aluminum panels on the exterior of existing buildings. this is achieved by folding aluminum panels with "tabbed" pieces that are slotted into a framing system mounted to the existing building wall.

now, the logic: A user will input a rectangular curve that will represent the face of the panel. from there, the right and left side have an additional tall, slender rectangle- this is the first part of the fold. on the outside of those rectangles, tabs are placed at uniform distances. those tabs will be slotted into the frame.

visually/in the grasshopper/rhino space, the panels should be flat, and have 3 distinct elements:

1. the face- this will be input by the user
2. the fold area- this will go on the sides of the face, outside of the face's area.
3. tabs sit outside the fold area.

I have included screenshots of the design for reference.

## Inputs:

boundary: user provided panel face boundary
fold width: this will be the area that is folded 90deg to either side. the user can input a numeric value here. the height is not an input because the fold area will be the same height as the panel boundary.
tab width: width of the tab (x axis)
tab height: the height of the tab (y axis)
tab spacing: this value will be the distance between tabs on center. the tabs will start in the exact middle of the height of the panel, and distance themselves from there. so if there is 1 tab, it will be centered. if there are 2 with spacing 36" on center, then the center of those tabs will be 18" each from the middle, so on. odd numbers will naturally always result in a center tab.

## Outputs:

panel face: simply the rectangle the user provided for the logic. output is to ensure all elements are preserved easily and well.
fold area
tabs

## Notes:

Below is a standard codeblock which should be placed above all created scripts. the information contained within it should reflect the script's contents. The code below should serve as a standard/example only.

Adhere strictly to written standards like spacing, capitalization, etc. 

Adhere strictly to naming conventions for the component, the component nickname, input naming, and output naming.

Adhere stricly to the standard for commenting information about the script's inputs/outputs and their input details so I can configure the component easily.

/// CODE BELOW ///

"""
Creates a grid of individual closed diamond cells within a region.

Inputs:
    boundary: Geometry (item access, crv)
    size_x: Number (item access, float)
    size_y: Number (item access, float)

Outputs:
    diagrid: List of Curves (The final individual closed diamond cells)
    bnd_rect: Curve (The bounding rectangle of the original input)
"""

try:
    ghenv.Component.Name = "BoundDiaGrid"
    ghenv.Component.NickName = "BndDiaG"
    ghenv.Component.Description = "Creates a grid of individual closed diamond cells within a region."
except NameError:
    pass

/// END ///