"""
Creates a grid of individual closed rectangular cells within a region.

Inputs:
    boundary: Geometry (item access, crv)
    size_x: Number (item access, float)
    size_y: Number (item access, float)

Outputs:
    rectgrid: List of Curves (The final individual closed rectangular cells)
    bnd_rect: Curve (The bounding rectangle of the original input)
"""

try:
    ghenv.Component.Name = "BoundRectGrid"
    ghenv.Component.NickName = "BRG"
    ghenv.Component.Description = "Creates a grid of individual closed rectangular cells within a region."
except NameError:
    pass

import Rhino.Geometry as rg

def create_closed_rect_cells(region_geometry, size_x_val, size_y_val):
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

    final_rects = []
    tol = 1e-5

    for row in range(-2, cells_y + 4):
        cy = p_min.Y + (actual_dy / 2.0) + (row * actual_dy)

        for col in range(-2, cells_x + 4):
            cx = p_min.X + (actual_dx / 2.0) + (col * actual_dx)

            if (cx - actual_dx/2.0 >= p_min.X - tol and
                cx + actual_dx/2.0 <= p_max.X + tol and
                cy - actual_dy/2.0 >= p_min.Y - tol and
                cy + actual_dy/2.0 <= p_max.Y + tol):

                pt0 = rg.Point3d(cx - actual_dx/2.0, cy - actual_dy/2.0, 0)
                pt1 = rg.Point3d(cx + actual_dx/2.0, cy - actual_dy/2.0, 0)
                pt2 = rg.Point3d(cx + actual_dx/2.0, cy + actual_dy/2.0, 0)
                pt3 = rg.Point3d(cx - actual_dx/2.0, cy + actual_dy/2.0, 0)

                pline = rg.Polyline([pt0, pt1, pt2, pt3, pt0])
                final_rects.append(rg.PolylineCurve(pline))

    return final_rects, bnd_rect_curve

if 'boundary' in globals() and 'size_x' in globals() and 'size_y' in globals():
    rectgrid, bnd_rect = create_closed_rect_cells(boundary, size_x, size_y)
