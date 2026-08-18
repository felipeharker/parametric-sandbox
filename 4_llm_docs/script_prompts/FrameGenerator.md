# Frame Generator

## Objectives

The frame for the panel mounting system uses a product known as a hat channel. these are aluminum pieces we fold and fabricate in house. the geometry may be complex to create, and i have included some images of their typical design for reference.

## Inputs:

frame face: this is an input which is taken from FrameTabSystem
frame tabs: also taken from FrameTabSystem. combined they will create the face surface of the hat channel
frame total width
frame total depth
fold angle: angle of the fold in degrees

## Outputs:

frame: open surfaces representing the frame


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