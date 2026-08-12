"""
Utility to generate Voronoi cells from points evaluated within a list of grid cells.

Inputs:
    grid_cells: List of Geometry (Surfaces, Breps, or Closed Curves)
    boundary: Curve (A single boundary curve to clip the entire Voronoi pattern)
    min_eval: Float (Minimum value to evaluate reparameterized surface, between 0 and 1)
    max_eval: Float (Maximum value to evaluate reparameterized surface, between 0 and 1)
    seed: Integer (Seed for random value generation)

Outputs:
    voronoi_cells: List of Curves (The generated Voronoi cells based on the evaluated points)
"""

try:
    ghenv.Component.Name = "GridToVoronoi"
    ghenv.Component.NickName = "GridVoronoi"
    ghenv.Component.Description = "Generates Voronoi cells by randomly evaluating normalized coordinates within a set of grid surfaces."
except NameError:
    pass

import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp
import random

# Initialize output
voronoi_cells = []

# Ensure inputs exist
if grid_cells and boundary and min_eval is not None and max_eval is not None and seed is not None:
    
    # Clamp eval values between 0 and 1
    min_eval = max(0.0, min(1.0, min_eval))
    max_eval = max(0.0, min(1.0, max_eval))
    
    random.seed(seed)
    num_cells = len(grid_cells)
    
    # Generate random evaluation values
    random_vals = [random.uniform(min_eval, max_eval) for _ in range(num_cells * 2)]
    u_vals = random_vals[:num_cells]
    v_vals = random_vals[num_cells:]
    
    evaluated_points = []
    
    for i, cell in enumerate(grid_cells):
        srf = None
        
        # Unwrap Grasshopper data types
        geom = cell.Value if hasattr(cell, 'Value') else cell
            
        # 1. ROBUST GEOMETRY HANDLING: Automatically accept Surfaces, Breps, or Curves
        if isinstance(geom, rg.Brep) and geom.Faces.Count > 0:
            srf = geom.Faces[0]
        elif isinstance(geom, rg.Surface):
            srf = geom
        elif isinstance(geom, rg.Curve) and geom.IsClosed and geom.IsPlanar():
            # If a curve (like your hexgrid) is passed, make it a temporary surface
            breps = rg.Brep.CreatePlanarBreps(geom, 0.001)
            if breps and len(breps) > 0:
                srf = breps[0].Faces[0]
                
        # Evaluate if a surface was successfully found or created
        if srf:
            u_domain = srf.Domain(0)
            v_domain = srf.Domain(1)
            
            u_mapped = u_domain.Min + (u_vals[i] * (u_domain.Max - u_domain.Min))
            v_mapped = v_domain.Min + (v_vals[i] * (v_domain.Max - v_domain.Min))
            
            pt = srf.PointAt(u_mapped, v_mapped)
            evaluated_points.append(pt)
            
    # Generate Voronoi if points exist
    if evaluated_points:
        # 2. ROBUST BOUNDARY HANDLING: Force boundary into a Rectangle3d
        bnd_geom = boundary.Value if hasattr(boundary, 'Value') else boundary
        bnd_box = bnd_geom.GetBoundingBox(True)
        
        x_interval = rg.Interval(bnd_box.Min.X, bnd_box.Max.X)
        y_interval = rg.Interval(bnd_box.Min.Y, bnd_box.Max.Y)
        bnd_rect = rg.Rectangle3d(rg.Plane.WorldXY, x_interval, y_interval)
        
        # Generate Voronoi using positional arguments to prevent kwarg misfires
        v_cells = ghcomp.Voronoi(evaluated_points, None, bnd_rect)
        
        if v_cells:
            voronoi_cells = v_cells