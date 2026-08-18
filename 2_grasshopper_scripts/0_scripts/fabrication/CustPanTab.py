"""
Creates fold areas and tabs for an aluminum panel system based on a face boundary,
using a custom user-defined tab geometry.

Inputs:
    boundary: Geometry (item access, crv)
    fold_width: Number (item access, float)
    tab_geo: Geometry (item access, crv) - The custom curve used for tab profiles
    tab_spacing: Number (item access, float)

Outputs:
    panel_face: Curve (The original panel face rectangle)
    fold: List of Curves (The left and right fold areas)
    tabs: List of Curves (The mapped custom tab geometry on the outside of the fold areas)
"""

import Rhino.Geometry as rg
import math

try:
    ghenv.Component.Name = "CustomPanelTabSystem"
    ghenv.Component.NickName = "CustPanTab"
    ghenv.Component.Description = "Creates fold areas and custom tabs for an aluminum panel system."
except NameError:
    pass

def create_panel_system(boundary, fold_width, tab_geo, tab_spacing):
    # Data validation
    if not boundary or fold_width is None or tab_geo is None or tab_spacing is None:
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

    # --- Setup the Custom Tab Base Plane ---
    # Find the planar orientation of the custom tab
    tab_rc, tab_plane = tab_geo.TryGetPlane()
    if not tab_rc:
        tab_plane = rg.Plane.WorldXY
        
    # We use the bounding box to find the left-most midpoint as our attachment anchor
    tab_bbox = tab_geo.GetBoundingBox(tab_plane)
    anchor_x = tab_bbox.Min.X
    anchor_y = (tab_bbox.Min.Y + tab_bbox.Max.Y) / 2.0
    
    # Create the base plane centered exactly on the tab's attachment point
    tab_anchor_pt = tab_plane.PointAt(anchor_x, anchor_y, 0)
    base_tab_plane = rg.Plane(tab_anchor_pt, tab_plane.XAxis, tab_plane.YAxis)
            
    # --- Generate left and right tab curves at each center height ---
    for cy in centers:
        
        # RIGHT TAB
        # Set the target plane on the right edge of the right fold
        right_pt = plane.PointAt(max_x + fold_width, cy, 0)
        right_plane = rg.Plane(right_pt, plane.XAxis, plane.YAxis)
        
        # Transform (Orient) from the base tab plane to the right plane
        xform_right = rg.Transform.PlaneToPlane(base_tab_plane, right_plane)
        right_tab = tab_geo.Duplicate()
        right_tab.Transform(xform_right)
        tabs.append(right_tab)
        
        
        # LEFT TAB
        # Reverse the X-Axis so the tab mirrors properly and faces outward (negative X)
        neg_x = rg.Vector3d(plane.XAxis)
        neg_x.Reverse()
        
        # Set the target plane on the left edge of the left fold
        left_pt = plane.PointAt(min_x - fold_width, cy, 0)
        left_plane = rg.Plane(left_pt, neg_x, plane.YAxis)
        
        # Transform (Orient) from the base tab plane to the flipped left plane
        xform_left = rg.Transform.PlaneToPlane(base_tab_plane, left_plane)
        left_tab = tab_geo.Duplicate()
        left_tab.Transform(xform_left)
        tabs.append(left_tab)
            
    return panel_face, fold, tabs

panel_face, fold, tabs = create_panel_system(boundary, fold_width, tab_geo, tab_spacing)