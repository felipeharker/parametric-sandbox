# Frame Tab System

## Objectives

The frame for the folded panels can also be defined parametrically. instead of tabs sticking out of the panel, the framing system has rectangular perforations where those tabs sit. 

## Inputs:

frame height: total height of the hat channel frame
face width: width of the top (flat) face of the hat channel
tab height: height of the opening
tab width: width of the opening
tab space x: calculated on center and starting at the middle of the face, this is the distance between the 2 openings on the x axis. there will always be exactly 2 tabs per set.
tab space y: distance between sets of openings calculated on center and starting at the middle of the face. this is the vertical/y axis distance between openings. similar to the panel tab placement logic


## Outputs:

frame face: rectangular frame face
tabs: curves representing the newly created tabs


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