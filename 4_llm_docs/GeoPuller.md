# Geometry Pulling Utility

## Objective:

Create a script which allows a user to wire the name of a layer (format is always layer::sublayer for sublayer access) to the component and "run" it using a boolean button. the component will then output any geometry on said layer

## Inputs:

- layer name: text input for the name of the layer where objects will be pulled.
- pull: boolean to run the script

## Outputs:

- Geo: the pulled rhino geometery

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