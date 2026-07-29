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
    ghenv.Component.NickName = "BDG"
    ghenv.Component.Description = "Creates a grid of individual closed diamond cells within a region."
except NameError:
    pass

import Rhino.Geometry as rg

def create_closed_diamond_cells(region_geometry, size_x_val, size_y_val):
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

    final_diamonds = []
    tol = 1e-5 

    for row in range(-2, (cells_y * 2) + 4):
        cy = p_min.Y + (actual_dy / 2.0) + (row * (actual_dy / 2.0))
        
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
                
                pt0 = rg.Point3d(cx - actual_dx/2.0, cy, 0)
                pt1 = rg.Point3d(cx, cy - actual_dy/2.0, 0)
                pt2 = rg.Point3d(cx + actual_dx/2.0, cy, 0)
                pt3 = rg.Point3d(cx, cy + actual_dy/2.0, 0)
                pt4 = rg.Point3d(cx - actual_dx/2.0, cy, 0)
                
                pline = rg.Polyline([pt0, pt1, pt2, pt3, pt4])
                final_diamonds.append(rg.PolylineCurve(pline))

    return final_diamonds, bnd_rect_curve

if 'boundary' in globals() and 'size_x' in globals() and 'size_y' in globals():
    diagrid, bnd_rect = create_closed_diamond_cells(boundary, size_x, size_y)
