"""
Generates a custom Voronoi pattern within grid cells based on scaled inner boundaries and evaluated curve points.
HIGH PERFORMANCE: Utilizes System.Threading.Tasks for concurrent multi-core processing.

Inputs:
    grid_cells: List of Curves (Base grid cells to reference as boundaries)
    inner_scale: Float (Scale factor between 0.0 and 1.0 for the inner cell)
    eval_outer: Float (Evaluation parameter between 0.0 and 1.0 for outer cell edges)
    eval_inner: Float (Evaluation parameter between 0.0 and 1.0 for inner cell edges)
    point_toggle: List of Booleans (7-item list of 0s and 1s activating specific generator points)

Outputs:
    pattern_curves: DataTree of Curves (The final generated Voronoi pattern curves, organized by grid cell)
"""

try:
    ghenv.Component.Name = "PatternGenerator"
    ghenv.Component.NickName = "PattGen"
    ghenv.Component.Description = "Generates a custom Voronoi pattern utilizing parallel multi-threading for maximum speed."
except NameError:
    pass

import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp
import ghpythonlib.treehelpers as th
import System.Threading.Tasks as tasks # The key to multi-threading

def generate_points(cell, inner_scale, eval_outer, eval_inner, toggle):
    pts = []
    
    amp = rg.AreaMassProperties.Compute(cell)
    if not amp: return []
    centroid = amp.Centroid
    
    if toggle[0]: pts.append(centroid)
        
    xform = rg.Transform.Scale(centroid, inner_scale)
    inner_cell = cell.DuplicateCurve()
    inner_cell.Transform(xform)
    
    outer_segments = cell.DuplicateSegments()
    inner_segments = inner_cell.DuplicateSegments()
    
    if outer_segments:
        if toggle[1]:
            for seg in outer_segments: pts.append(seg.PointAtNormalizedLength(0.5))
        if toggle[2]:
            for seg in outer_segments: pts.append(seg.PointAtStart)
        if toggle[3]:
            for seg in outer_segments: pts.append(seg.PointAtNormalizedLength(eval_outer))
                
    if inner_segments:
        if toggle[4]:
            for seg in inner_segments: pts.append(seg.PointAtNormalizedLength(0.5))
        if toggle[5]:
            for seg in inner_segments: pts.append(seg.PointAtStart)
        if toggle[6]:
            for seg in inner_segments: pts.append(seg.PointAtNormalizedLength(eval_inner))
                
    return pts

# --- MAIN EXECUTION ---
tolerance = 0.001 

# Pre-allocate a list of empty lists the exact size of grid_cells to avoid memory reallocation
nested_curves = [[] for _ in range(len(grid_cells))] if grid_cells else []

def process_cell(i):
    """ This function will be executed simultaneously across all your CPU cores """
    cell = grid_cells[i]
    if not isinstance(cell, rg.Curve) or not cell.IsClosed:
        return
        
    success, plane = cell.TryGetPlane()
    if not success: plane = rg.Plane.WorldXY
        
    # Generate and cull points
    cell_points = generate_points(cell, inner_scale, eval_outer, eval_inner, point_toggle)
    if not cell_points: return
    
    clean_points = rg.Point3d.CullDuplicates(cell_points, tolerance) if len(cell_points) > 1 else cell_points
        
    if clean_points and len(clean_points) >= 2:
        
        # Bounding box logic
        bbox = cell.GetBoundingBox(True)
        bbox.Inflate(0.5) 
        
        c1 = rg.Point3d(bbox.Min.X, bbox.Min.Y, 0)
        c2 = rg.Point3d(bbox.Max.X, bbox.Min.Y, 0)
        c3 = rg.Point3d(bbox.Max.X, bbox.Max.Y, 0)
        c4 = rg.Point3d(bbox.Min.X, bbox.Max.Y, 0)
        bbox_crv = rg.Polyline([c1, c2, c3, c4, c1]).ToNurbsCurve()
        
        # Voronoi generation
        v_cells_raw = ghcomp.Voronoi(clean_points, boundary=bbox_crv)
        if isinstance(v_cells_raw, rg.Curve): v_cells = [v_cells_raw]
        elif v_cells_raw: v_cells = list(v_cells_raw)
        else: return
            
        trimmed_cells = []
        for v_c in v_cells:
            if not v_c.IsClosed: continue 
            
            # Topological math check (much faster than booleans)
            rel = rg.Curve.PlanarClosedCurveRelationship(cell, v_c, plane, tolerance)
            
            if rel == rg.RegionContainment.BInsideA:
                trimmed_cells.append(v_c)
                
            elif rel == rg.RegionContainment.MutualIntersection or rel == rg.RegionContainment.AInsideB:
                # Only boolean what absolutely must be booleaned
                intersections = rg.Curve.CreateBooleanIntersection(v_c, cell, tolerance)
                if intersections:
                    for int_crv in intersections:
                        if int_crv.IsClosed:
                            trimmed_cells.append(int_crv)
                            
        # Safely insert the final trimmed cells into their exact index position
        nested_curves[i] = trimmed_cells

# Initialize the parallel processing loop
if grid_cells and len(point_toggle) == 7:
    # tasks.Parallel.For takes a start index, end index, and the function to run concurrently
    tasks.Parallel.For(0, len(grid_cells), process_cell)

# Convert the cleanly ordered nested list into a Grasshopper DataTree
pattern_curves = th.list_to_tree(nested_curves)