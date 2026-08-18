"""
Creates folded 3-dimensional gridded geometries efficiently from planar cells and fold lines.

Inputs:
    grid_cells: List of Curves (list access, closed crv)
    fold_lines: DataTree of Curves (tree access, open crv)
    fold_angle: Number (item access, float)

Outputs:
    folded_cells: List of Breps (The final 3D folded geometries)
"""

import Rhino.Geometry as rg
import math
import scriptcontext as sc
import Grasshopper as gh

try:
    ghenv.Component.Name = "GridFoldPlanar"
    ghenv.Component.NickName = "GridFPlan"
    ghenv.Component.Description = "Creates folded 3D gridded geometries efficiently."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Folding"
    ghenv.Component.Message = ""
except NameError:
    pass

folded_cells = []
tol = sc.doc.ModelAbsoluteTolerance

if grid_cells and fold_lines and fold_angle is not None:
    # Convert input angle from degrees to radians
    angle_rad = math.radians(fold_angle)
    
    # OPTIMIZATION 1: Check if DataTree branches perfectly match the list of cells
    # This allows us to use O(1) Index matching instead of O(N^2) Spatial searching
    match_trees = fold_lines.BranchCount == len(grid_cells)
    
    # Fallback to a flat list just in case you flatten the tree in the future
    flat_fold_lines = []
    if not match_trees:
        if hasattr(fold_lines, 'AllData'):
            flat_fold_lines = fold_lines.AllData()
        else:
            flat_fold_lines = fold_lines

    for i, cell in enumerate(grid_cells):
        if not cell or not cell.IsClosed:
            continue
            
        # Create planar surface from cell
        breps = rg.Brep.CreatePlanarBreps(cell, tol)
        if not breps:
            continue
        base_brep = breps[0]
        
        # Determine the plane of the cell to establish a consistent normal
        success, plane = cell.TryGetPlane(tol)
        if not success:
            plane = rg.Plane.WorldXY
        normal = plane.ZAxis
            
        associated_lines = []
        if match_trees:
            # Grab lines directly by index (Instantaneous)
            associated_lines = fold_lines.Branch(i)
        else:
            # Fallback to slow spatial check ONLY if the data tree structure is broken/flattened
            for f_line in flat_fold_lines:
                if not f_line: continue
                mp = f_line.PointAtNormalizedLength(0.5)
                containment = cell.Contains(mp, plane, tol)
                if containment == rg.PointContainment.Inside or containment == rg.PointContainment.Coincident:
                    associated_lines.append(f_line)
        
        if not associated_lines:
            folded_cells.append(base_brep)
            continue
            
        # Split the cell's face using the inner fold lines
        split_breps = base_brep.Split(associated_lines, tol)
        
        if not split_breps:
            folded_cells.append(base_brep)
            continue
            
        # Rotate each fragment around its outer bounding edge (the hinge)
        for s_brep in split_breps:
            hinge_edge = None
            
            for edge in s_brep.Edges:
                edge_mp = edge.PointAtNormalizedLength(0.5)
                success, t = cell.ClosestPoint(edge_mp)
                if success and edge_mp.DistanceTo(cell.PointAt(t)) <= tol * 10:
                    hinge_edge = edge
                    break
                    
            if hinge_edge:
                # OPTIMIZATION 2: Simple arithmetic average instead of AreaMassProperties
                # This mathematically finds a localized "center" point instantaneously 
                vertices = s_brep.Vertices
                pt_sum = rg.Point3d.Origin
                for v in vertices:
                    pt_sum += v.Location
                face_center = pt_sum / vertices.Count
                
                edge_mp = hinge_edge.PointAtNormalizedLength(0.5)
                
                # Define initial rotation axis based on the hinge line
                axis_vec = hinge_edge.PointAtEnd - hinge_edge.PointAtStart
                vec_inward = face_center - edge_mp
                
                # Use Cross Product to guarantee uniform "Up" folding
                cross = rg.Vector3d.CrossProduct(axis_vec, vec_inward)
                if cross * normal < 0:
                    axis_vec.Reverse()
                
                center_pt = hinge_edge.PointAtStart
                
                # Apply rotation 
                xform = rg.Transform.Rotation(angle_rad, axis_vec, center_pt)
                s_brep.Transform(xform)
                
            folded_cells.append(s_brep)