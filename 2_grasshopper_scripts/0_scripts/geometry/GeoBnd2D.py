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
    ghenv.Component.Name = "GeometryBoundary2D"
    ghenv.Component.NickName = "GeoBnd2D"
    ghenv.Component.Description = "Draws a boundary rectangle around a geometry based on a user-defined plane."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Geometry"
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