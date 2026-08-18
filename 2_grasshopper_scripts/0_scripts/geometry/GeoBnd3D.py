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
    ghenv.Component.Name = "GeometryBoundary3D"
    ghenv.Component.NickName = "GeoBnd3D"
    ghenv.Component.Description = "Draws a boundary box around a geometry."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Geometry"
    ghenv.Component.Message = ""
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