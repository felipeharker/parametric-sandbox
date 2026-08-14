"""
Creates a grid of individual closed triangular cells within a region.

Inputs:
    boundary: Geometry (item access, crv)
    size_x: Number (item access, float)
    size_y: Number (item access, float)

Outputs:
    trigrid: List of Curves (The final individual closed triangular cells)
    bnd_rect: Curve (The bounding rectangle of the original input)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "BoundTriGrid"
    ghenv.Component.NickName = "BndTriG"
    ghenv.Component.Description = "Creates a grid of individual closed triangular cells within a region."

    # --- Inputs Metadata ---
    # Index 0: boundary
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "boundary"
        ghenv.Component.Params.Input[0].NickName = "Bnd"
        ghenv.Component.Params.Input[0].Description = "Geometry (item access, crv)"

    # Index 1: size_x
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "size_x"
        ghenv.Component.Params.Input[1].NickName = "Sx"
        ghenv.Component.Params.Input[1].Description = "Number (item access, float)"

    # Index 2: size_y
    if ghenv.Component.Params.Input.Count > 2:
        ghenv.Component.Params.Input[2].Name = "size_y"
        ghenv.Component.Params.Input[2].NickName = "Sy"
        ghenv.Component.Params.Input[2].Description = "Number (item access, float)"

    # --- Outputs Metadata ---
    # Index 0: trigrid
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "trigrid"
        ghenv.Component.Params.Output[0].NickName = "Tri"
        ghenv.Component.Params.Output[0].Description = "List of Curves (The final individual closed triangular cells)"

    # Index 1: bnd_rect
    if ghenv.Component.Params.Output.Count > 1:
        ghenv.Component.Params.Output[1].Name = "bnd_rect"
        ghenv.Component.Params.Output[1].NickName = "Rect"
        ghenv.Component.Params.Output[1].Description = "Curve (The bounding rectangle of the original input)"

except NameError:
    pass

import Rhino.Geometry as rg

def create_closed_triangular_cells(region_geometry, size_x_val, size_y_val):
    if region_geometry is None: return [], None
    if size_x_val <= 0 or size_y_val <= 0: return [], None

    bbox = region_geometry.GetBoundingBox(rg.Plane.WorldXY)
    if not bbox.IsValid: return [], None

    p_min = bbox.Min
    p_max = bbox.Max

    pt_bl = rg.Point3d(p_min.X, p_min.Y, 0)
    pt_br = rg.Point3d(p_max.X, p_min.Y, 0)
    pt_tr = rg.Point3d(p_max.X, p_max.Y, 0)
    pt_tl = rg.Point3d(p_min.X, p_max.Y, 0)

    bnd_rect_curve = rg.PolylineCurve(rg.Polyline([pt_bl, pt_br, pt_tr, pt_tl, pt_bl]))

    width = p_max.X - p_min.X
    height = p_max.Y - p_min.Y

    if width <= 0 or height <= 0: return [], bnd_rect_curve

    cells_x = max(1, int(round(width / size_x_val)))
    cells_y = max(1, int(round(height / size_y_val)))

    actual_dx = width / float(cells_x)
    actual_dy = height / float(cells_y)

    final_triangles = []
    tol = 1e-5

    for row in range(cells_y):
        y_start = p_min.Y + (row * actual_dy)
        y_end = y_start + actual_dy

        for col in range(cells_x):
            x_start = p_min.X + (col * actual_dx)
            x_end = x_start + actual_dx

            if (x_start >= p_min.X - tol and
                x_end <= p_max.X + tol and
                y_start >= p_min.Y - tol and
                y_end <= p_max.Y + tol):

                # Define the four corners of the current rectangular cell
                pt0 = rg.Point3d(x_start, y_start, 0) # Bottom-Left
                pt1 = rg.Point3d(x_end, y_start, 0)   # Bottom-Right
                pt2 = rg.Point3d(x_end, y_end, 0)     # Top-Right
                pt3 = rg.Point3d(x_start, y_end, 0)   # Top-Left

                # Alternate the diagonal split to create a continuous triangular diagrid pattern
                if (row + col) % 2 == 0:
                    # Split from Top-Left to Bottom-Right (\)
                    pline1 = rg.Polyline([pt0, pt1, pt3, pt0])
                    pline2 = rg.Polyline([pt1, pt2, pt3, pt1])
                else:
                    # Split from Bottom-Left to Top-Right (/)
                    pline1 = rg.Polyline([pt0, pt1, pt2, pt0])
                    pline2 = rg.Polyline([pt0, pt2, pt3, pt0])

                final_triangles.append(rg.PolylineCurve(pline1))
                final_triangles.append(rg.PolylineCurve(pline2))

    return final_triangles, bnd_rect_curve

if 'boundary' in globals() and 'size_x' in globals() and 'size_y' in globals():
    trigrid, bnd_rect = create_closed_triangular_cells(boundary, size_x, size_y)