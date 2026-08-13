# Geometry Baking Utility

## Objective:

Create a script which allows a user to wire a geometry (curve, surface, 3D geometries, etc) into a script which bakes the wired geometry into rhino using a boolean button. User will have some control over configs and settings of the layer, which will be outlined below.

## Inputs:

- geometry: input that accepts any sort of geometric data
- layer name: text input for the name of the layer where objects will be baked. if the layer does not already exist, it shall be created upon running the script. to create a sublayer from this script, the user will use the layer::sublayer syntax.
- add/replace: boolean toggle which either replaces all existing contents of a layer with the wired geometry, or adds the wired geometry to the layer. 1 = add, 0 = replace
- bake: boolean to run the script (likely wired to a button)

## Outputs:

- there are no outputs for this component, only baked objects in rhino.

## Note:

names, nicknames, inputs, and output names can and should be changed to adhere to the standard outlined (attached below)

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