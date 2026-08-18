"""
Creates fold areas and tabs for an aluminum panel system based on a face boundary.

Inputs:
    boundary: Geometry (item access, crv)
    fold_width: Number (item access, float)
    tab_width: Number (item access, float)
    tab_height: Number (item access, float)
    tab_spacing: Number (item access, float)

Outputs:
    panel_face: Curve (The original panel face rectangle)
    fold: List of Curves (The left and right fold areas)
    tabs: List of Curves (The tab geometry on the outside of the fold areas)
"""

import Rhino.Geometry as rg
import math

try:
    ghenv.Component.Name = "PanelTabSystem"
    ghenv.Component.NickName = "PanTab"
    ghenv.Component.Description = "Creates fold areas and tabs for an aluminum panel system based on a face boundary."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Fabrication"
except NameError:
    pass

def create_panel_system(boundary, fold_width, tab_width, tab_height, tab_spacing):
    # Data validation
    if not boundary or fold_width is None or tab_width is None or tab_height is None or tab_spacing is None:
        return None, [], []
        
    # Attempt to get the local plane of the boundary curve to ensure it works in 3D space
    rc, plane = boundary.TryGetPlane()
    if not rc:
        plane = rg.Plane.WorldXY
        
    # Get bounding box aligned to the valid plane
    bbox = boundary.GetBoundingBox(plane)
    
    min_x = bbox.Min.X
    max_x = bbox.Max.X
    min_y = bbox.Min.Y
    max_y = bbox.Max.Y
    
    height = max_y - min_y
    
    # 1. Panel Face Output
    panel_face = boundary
    
    # 2. Fold Areas Output
    fold = []
    
    # Left Fold
    left_fold_x = rg.Interval(min_x - fold_width, min_x)
    y_int = rg.Interval(min_y, max_y)
    left_fold = rg.Rectangle3d(plane, left_fold_x, y_int).ToNurbsCurve()
    fold.append(left_fold)
    
    # Right Fold
    right_fold_x = rg.Interval(max_x, max_x + fold_width)
    right_fold = rg.Rectangle3d(plane, right_fold_x, y_int).ToNurbsCurve()
    fold.append(right_fold)
    
    # 3. Tabs Output
    tabs = []
    
    # Determine the number of tabs based on spacing and height
    num_tabs = max(1, int(round(height / tab_spacing)))
    
    mid_y = min_y + (height / 2.0)
    centers = []
    
    # Calculate tab centerpoints expanding outward from the middle
    if num_tabs % 2 == 1:
        # Odd number of tabs (1 center tab + mirrored pairs)
        half_count = num_tabs // 2
        for i in range(-half_count, half_count + 1):
            centers.append(mid_y + i * tab_spacing)
    else:
        # Even number of tabs (mirrored pairs offset from center)
        half_count = num_tabs // 2
        for i in range(1, half_count + 1):
            centers.append(mid_y + (i - 0.5) * tab_spacing)
            centers.append(mid_y - (i - 0.5) * tab_spacing)
            
    # Generate left and right tab curves at each center height
    for cy in centers:
        tab_y_int = rg.Interval(cy - tab_height / 2.0, cy + tab_height / 2.0)
        
        # Left Tab
        left_tab_x = rg.Interval(min_x - fold_width - tab_width, min_x - fold_width)
        left_tab = rg.Rectangle3d(plane, left_tab_x, tab_y_int).ToNurbsCurve()
        tabs.append(left_tab)
        
        # Right Tab
        right_tab_x = rg.Interval(max_x + fold_width, max_x + fold_width + tab_width)
        right_tab = rg.Rectangle3d(plane, right_tab_x, tab_y_int).ToNurbsCurve()
        tabs.append(right_tab)
        
    return panel_face, fold, tabs

panel_face, fold, tabs = create_panel_system(boundary, fold_width, tab_width, tab_height, tab_spacing)