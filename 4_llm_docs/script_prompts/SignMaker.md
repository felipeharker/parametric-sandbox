# Sign Maker

## Objectives:

This script is a commercial signage design assistant, essentially. For now, let's focus on front and reverse illuminated signage only, channel letters. The elements of a channel letter are: sidewall depth, standoff from wall, and illumination. there are 2 kinds of illumination, front and reverse lit. I will go into more detail below. note, we will operate on the assumption the signage is designed on the xy-plane for now, so movements, extrusions, etc. will be in the z direction.

## Inputs:

curves: input the sign curves here
sidewall depth: the depth of the design's walls. this is an extrusion value in the z
standoff distance: this is the distance which the sign will be moved from the wall. this is a move value in the z
illumination: integer values where 0 = non-illuminated, 1 = front illuminated, and 2 = reverse illuminated
* the differences in illumination are important, but the surfaces will behave similarly. for illumination = 1, please create an open surface 1/32" ABOVE (positive z) the extruded and moved sign body.
For illumination = 2, please create an open surface 1/32" BELOW (negative z) the extruded and moved sign body. for Illumination = 0, no surfaces are placed.

## Outputs:

sign curves: the originally input sign curves in their original position
sign body: the extruded and moved geometry of the sign
sign faces: the open surface faces of the illuminated signage

## Model Notes:

Sometimes, it can be challenging to describe verbally how a design/workflow should function and what the desired outcome is. if anything, no matter how small or large, is unclear, ambigious, or unspecified, ALWAYS ask for clarification instead of making assumptions and potentially outputting buggy code.

## Code and Output Notes:

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