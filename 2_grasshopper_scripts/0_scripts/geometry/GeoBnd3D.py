"""
Draws a boundary box around a geometry.

Inputs:
    geo: Geometry (item access, geo)

Outputs:
    bnd_box: Box (The 3D bounding box of the original geometry)
    x: Number (Dimension in the first axis)
    y: Number (Dimension in the second axis)
    z: Number (Dimension in the third axis)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "GeometryBoundary3D"
    ghenv.Component.NickName = "GeoBnd3D"
    ghenv.Component.Description = "Draws a boundary box around a geometry."

    # --- Inputs Metadata ---
    # Index 0: geo
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "geo"
        ghenv.Component.Params.Input[0].NickName = "Geo"
        ghenv.Component.Params.Input[0].Description = "Geometry (item access, geo)"

    # --- Outputs Metadata ---
    # Index 0: bnd_box
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "bnd_box"
        ghenv.Component.Params.Output[0].NickName = "BndBo"
        ghenv.Component.Params.Output[0].Description = "Box (The 3D bounding box of the original geometry)"

    # Index 1: x
    if ghenv.Component.Params.Output.Count > 1:
        ghenv.Component.Params.Output[1].Name = "x"
        ghenv.Component.Params.Output[1].NickName = "X"
        ghenv.Component.Params.Output[1].Description = "Number (Dimension in the first axis)"

    # Index 2: y
    if ghenv.Component.Params.Output.Count > 2:
        ghenv.Component.Params.Output[2].Name = "y"
        ghenv.Component.Params.Output[2].NickName = "Y"
        ghenv.Component.Params.Output[2].Description = "Number (Dimension in the second axis)"

    # Index 3: z
    if ghenv.Component.Params.Output.Count > 3:
        ghenv.Component.Params.Output[3].Name = "z"
        ghenv.Component.Params.Output[3].NickName = "Z"
        ghenv.Component.Params.Output[3].Description = "Number (Dimension in the third axis)"

except NameError:
    pass

import Rhino.Geometry as rg

def create_bounding_box(geometry):
    """
    Calculates the world-aligned 3D bounding box of a geometry.
    """
    # Get the world-aligned bounding box of the geometry
    bbox = geometry.GetBoundingBox(True)

    if not bbox.IsValid:
        return None, None, None, None

    # Convert BoundingBox to a Box geometry
    box = rg.Box(bbox)

    # Extract dimensions using the Min and Max points
    dim_x = bbox.Max.X - bbox.Min.X
    dim_y = bbox.Max.Y - bbox.Min.Y
    dim_z = bbox.Max.Z - bbox.Min.Z

    return box, dim_x, dim_y, dim_z

# Initialize outputs
bnd_box = None
x = None
y = None
z = None

# Execute if input is provided
if geo:
    bnd_box, x, y, z = create_bounding_box(geo)