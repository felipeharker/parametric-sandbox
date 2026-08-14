"""
Creates a grid of individual closed hexagonal cells within a region.

Inputs:
    boundary: Geometry (item access, crv)
    size_x: Number (item access, float)
    size_y: Number (item access, float)

Outputs:
    hexgrid: List of Curves (The final individual closed hexagonal cells)
    bnd_rect: Curve (The bounding rectangle of the original input)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "BoundHexGrid"
    ghenv.Component.NickName = "BndHexG"
    ghenv.Component.Description = "Creates a grid of individual closed hexagonal cells within a region."

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
    # Index 0: hexgrid
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "hexgrid"
        ghenv.Component.Params.Output[0].NickName = "Hex"
        ghenv.Component.Params.Output[0].Description = "List of Curves (The final individual closed hexagonal cells)"

    # Index 1: bnd_rect
    if ghenv.Component.Params.Output.Count > 1:
        ghenv.Component.Params.Output[1].Name = "bnd_rect"
        ghenv.Component.Params.Output[1].NickName = "Rect"
        ghenv.Component.Params.Output[1].Description = "Curve (The bounding rectangle of the original input)"

except NameError:
    pass

import Rhino.Geometry as rg
import math

def create_closed_hex_cells(region_geometry, size_x_val, size_y_val):
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
    cells_y = max(1, int(round(height / (size_y_val * 0.75))))

    actual_dx = width / float(cells_x)
    actual_dy = height / float(cells_y)

    rx = actual_dx / math.sqrt(3.0)
    ry = actual_dy / 1.5

    final_hexes = []
    tol = 1e-5

    for row in range(-2, cells_y + 4):
        cy = p_min.Y + (actual_dy / 2.0) + (row * actual_dy)

        if row % 2 == 0:
            cx_start = p_min.X + (actual_dx / 2.0)
        else:
            cx_start = p_min.X + actual_dx

        for col in range(-2, cells_x + 4):
            cx = cx_start + col * actual_dx

            if (cx - actual_dx/2.0 >= p_min.X - tol and
                cx + actual_dx/2.0 <= p_max.X + tol and
                cy - actual_dy/2.0 >= p_min.Y - tol and
                cy + actual_dy/2.0 <= p_max.Y + tol):

                pts = []
                for k in range(6):
                    ang = math.radians(30.0 + 60.0 * k)
                    vx = cx + rx * math.cos(ang)
                    vy = cy + ry * math.sin(ang)
                    pts.append(rg.Point3d(vx, vy, 0.0))
                pts.append(pts[0])

                pline = rg.Polyline(pts)
                final_hexes.append(rg.PolylineCurve(pline))

    return final_hexes, bnd_rect_curve

if 'boundary' in globals() and 'size_x' in globals() and 'size_y' in globals():
    hexgrid, bnd_rect = create_closed_hex_cells(boundary, size_x, size_y)
