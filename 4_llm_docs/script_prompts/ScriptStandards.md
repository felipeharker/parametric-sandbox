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
    # --- Component Metadata ---
    ghenv.Component.Name = "BoundDiaGrid"
    ghenv.Component.NickName = "BndDiaG"
    ghenv.Component.Description = "Creates a grid of individual closed diamond cells within a region."

    # --- Inputs Metadata ---
    # Index 0: boundary
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "boundary"
        ghenv.Component.Params.Input[0].NickName = "Bnd" # Shortened nickname for the canvas
        ghenv.Component.Params.Input[0].Description = "Boundary curve to contain the diagrid (Geometry: crv)"

    # Index 1: size_x
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "size_x"
        ghenv.Component.Params.Input[1].NickName = "Sx"
        ghenv.Component.Params.Input[1].Description = "Diamond cell size in the X direction (Number: float)"

    # Index 2: size_y
    if ghenv.Component.Params.Input.Count > 2:
        ghenv.Component.Params.Input[2].Name = "size_y"
        ghenv.Component.Params.Input[2].NickName = "Sy"
        ghenv.Component.Params.Input[2].Description = "Diamond cell size in the Y direction (Number: float)"

    # --- Outputs Metadata ---
    # Index 0: diagrid
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "diagrid"
        ghenv.Component.Params.Output[0].NickName = "Dia"
        ghenv.Component.Params.Output[0].Description = "The final individual closed diamond cells (List of Curves)"

    # Index 1: bnd_rect
    if ghenv.Component.Params.Output.Count > 1:
        ghenv.Component.Params.Output[1].Name = "bnd_rect"
        ghenv.Component.Params.Output[1].NickName = "Rect"
        ghenv.Component.Params.Output[1].Description = "The bounding rectangle of the original input (Curve)"

except NameError:
    pass