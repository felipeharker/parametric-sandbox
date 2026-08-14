"""
Draws a boundary rectangle around a geometry based on a user-defined plane.

Inputs:
    geo: Geometry (item access, geo)
    plane: Plane (item access, plane)

Outputs:
    bnd_rect: Curve (The bounding rectangle aligned to the input plane)
    x: Number (Dimension in the first axis of the plane)
    y: Number (Dimension in the second axis of the plane)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "GeometryBoundary2D"
    ghenv.Component.NickName = "GeoBnd2D"
    ghenv.Component.Description = "Draws a boundary rectangle around a geometry based on a user-defined plane."

    # --- Inputs Metadata ---
    # Index 0: geo
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "geo"
        ghenv.Component.Params.Input[0].NickName = "Geo"
        ghenv.Component.Params.Input[0].Description = "Geometry (item access, geo)"

    # Index 1: plane
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "plane"
        ghenv.Component.Params.Input[1].NickName = "Pln"
        ghenv.Component.Params.Input[1].Description = "Plane (item access, plane)"

    # --- Outputs Metadata ---
    # Index 0: bnd_rect
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "bnd_rect"
        ghenv.Component.Params.Output[0].NickName = "Rect"
        ghenv.Component.Params.Output[0].Description = "Curve (The bounding rectangle aligned to the input plane)"

    # Index 1: x
    if ghenv.Component.Params.Output.Count > 1:
        ghenv.Component.Params.Output[1].Name = "x"
        ghenv.Component.Params.Output[1].NickName = "X"
        ghenv.Component.Params.Output[1].Description = "Number (Dimension in the first axis of the plane)"

    # Index 2: y
    if ghenv.Component.Params.Output.Count > 2:
        ghenv.Component.Params.Output[2].Name = "y"
        ghenv.Component.Params.Output[2].NickName = "Y"
        ghenv.Component.Params.Output[2].Description = "Number (Dimension in the second axis of the plane)"

except NameError:
    pass

import Rhino.Geometry as rg

def create_oriented_boundary(geometry, base_plane):
    """
    Calculates the bounding rectangle of a geometry aligned to a specific plane.
    """
    # Get the bounding box of the geometry oriented to the user-defined plane
    bbox = geometry.GetBoundingBox(base_plane)

    if not bbox.IsValid:
        return None, None, None

    # Extract the X and Y domains (intervals) from the local bounding box coordinates
    interval_x = rg.Interval(bbox.Min.X, bbox.Max.X)
    interval_y = rg.Interval(bbox.Min.Y, bbox.Max.Y)

    # Construct the rectangle on the given plane using the intervals
    rect = rg.Rectangle3d(base_plane, interval_x, interval_y)

    # Extract dimensions
    dim_x = interval_x.Length
    dim_y = interval_y.Length

    return rect.ToNurbsCurve(), dim_x, dim_y

# Initialize outputs
bnd_rect = None
x = None
y = None

# Execute if inputs are provided
if geo and plane:
    bnd_rect, x, y = create_oriented_boundary(geo, plane)