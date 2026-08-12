"""
Generates a custom Voronoi pattern within grid cells based on scaled inner boundaries and evaluated curve points.

Inputs:
    grid_cells: List of Curves (Base grid cells to reference as boundaries)
    inner_scale: Float (Scale factor between 0.0 and 1.0 for the inner cell)
    eval_outer: Float (Evaluation parameter between 0.0 and 1.0 for outer cell edges)
    eval_inner: Float (Evaluation parameter between 0.0 and 1.0 for inner cell edges)
    point_toggle: List of Booleans (7-item list of 0s and 1s activating specific generator points. 1=Centroid, 2=OuterMid, 3=OuterVert, 4=OuterEval, 5=InnerMid, 6=InnerVert, 7=InnerEval)

Outputs:
    pattern_curves: DataTree of Curves (The final generated Voronoi pattern curves, organized by grid cell)
"""

try:
    ghenv.Component.Name = "PatternGenerator"
    ghenv.Component.NickName = "PattGen"
    ghenv.Component.Description = "Generates a custom Voronoi pattern within grid cells based on scaled inner boundaries and evaluated curve points."
except NameError:
    pass

import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp
import ghpythonlib.treehelpers as th

def generate_points(cell, inner_scale, eval_outer, eval_inner, toggle):
    pts = []
    
    # Get Cell Centroid (Point 1)
    amp = rg.AreaMassProperties.Compute(cell)
    if not amp: return []
    centroid = amp.Centroid
    
    if toggle[0]:
        pts.append(centroid)
        
    # Generate Inner Cell
    xform = rg.Transform.Scale(centroid, inner_scale)
    inner_cell = cell.DuplicateCurve()
    inner_cell.Transform(xform)
    
    # Explode curves into individual segments
    outer_segments = cell.DuplicateSegments()
    inner_segments = inner_cell.DuplicateSegments()
    
    # --- OUTER CELL POINTS ---
    if outer_segments:
        if toggle[1]: # Point 2: Outer Midpoints
            for seg in outer_segments:
                pts.append(seg.PointAtNormalizedLength(0.5))
                
        if toggle[2]: # Point 3: Outer Vertices
            for seg in outer_segments:
                pts.append(seg.PointAtStart)
                
        if toggle[3]: # Point 4: Outer Evaluated Points
            for seg in outer_segments:
                pts.append(seg.PointAtNormalizedLength(eval_outer))
                
    # --- INNER CELL POINTS ---
    if inner_segments:
        if toggle[4]: # Point 5: Inner Midpoints
            for seg in inner_segments:
                pts.append(seg.PointAtNormalizedLength(0.5))
                
        if toggle[5]: # Point 6: Inner Vertices
            for seg in inner_segments:
                pts.append(seg.PointAtStart)
                
        if toggle[6]: # Point 7: Inner Evaluated Points
            for seg in inner_segments:
                pts.append(seg.PointAtNormalizedLength(eval_inner))
                
    return pts

# --- MAIN EXECUTION ---
nested_curves = []

# Validate inputs
if grid_cells and len(point_toggle) == 7:
    for cell in grid_cells:
        if not isinstance(cell, rg.Curve):
            continue
            
        # 1. Generate the combined list of points for this specific cell
        cell_points = generate_points(cell, inner_scale, eval_outer, eval_inner, point_toggle)
        
        # 2. Cull duplicate points (prevents Voronoi from throwing errors)
        if len(cell_points) > 1:
            clean_points = rg.Point3d.CullDuplicates(cell_points, 0.001)
        else:
            clean_points = cell_points
            
        # 3. Generate Voronoi if we have enough points
        if clean_points and len(clean_points) >= 2:
            v_cells = ghcomp.Voronoi(clean_points, boundary=cell)
            
            if isinstance(v_cells, rg.Curve):
                nested_curves.append([v_cells])
            elif v_cells:
                nested_curves.append(list(v_cells))
            else:
                nested_curves.append([])
        else:
            nested_curves.append([])

# Convert the nested list into a Grasshopper DataTree
pattern_curves = th.list_to_tree(nested_curves)