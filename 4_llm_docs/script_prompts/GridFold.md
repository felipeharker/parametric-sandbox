# Grid Fold

## Objectives:

A user will be able to create folded (3-dimensional) gridded geometries by inputting grid cell curves (closed) and "fold lines" which are open curves contained within the cell. these curves are used to split the face of the individual cell. the fold lines will serve as the axis upon which a surface will be rotated. the final input in this component is a numeric value equal to the angle which the new surfaces will be folded/rotated.

I have attached images for reference. please reference the images to understand the logic of the process, and not the materiality or scale, etc. just logic and process.

## Inputs:

grid cells: base grid cells
fold lines: lines for fold axis
fold angle: the angle of the fold of each surface

## Outputs:

folded grid cells

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