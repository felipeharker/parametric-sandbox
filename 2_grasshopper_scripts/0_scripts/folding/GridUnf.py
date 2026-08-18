"""
Unrolls 3D folded geometries into 2D cut and fold linework for fabrication.

Inputs:
    grid_cells: List of Breps (list access, folded 3D geometries, faces, or solids)
    spacing: Number (item access, float)

Outputs:
    cut_lines: DataTree of Curves (Outer boundaries of the flattened shapes)
    fold_lines: DataTree of Curves (Internal fold/hinge lines)
"""

import Rhino.Geometry as rg
import scriptcontext as sc
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
import System

try:
    ghenv.Component.Name = "GridUnfold"
    ghenv.Component.NickName = "GridUnf"
    ghenv.Component.Description = "Unrolls 3D folded geometries into 2D cut and fold linework for fabrication."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Folding"
    ghenv.Component.Message = ""
except NameError:
    pass

cut_lines = DataTree[System.Object]()
fold_lines = DataTree[System.Object]()

tol = sc.doc.ModelAbsoluteTolerance

if grid_cells:
    # Set default array spacing if no input is provided
    space_val = 10.0 if spacing is None else spacing
    
    # REQUIREMENT 1 & 2: Handle unjoined faces and closed solids
    # JoinBreps absorbs all coincident/touching faces into individual contiguous polysurfaces
    joined_breps = rg.Brep.JoinBreps(grid_cells, tol)
    
    # Fallback in case JoinBreps fails (e.g. if the list already consists of distinct closed solids)
    if not joined_breps:
        joined_breps = grid_cells
        
    current_x = 0.0
    
    for i, j_brep in enumerate(joined_breps):
        if not j_brep or not j_brep.IsValid:
            continue
            
        # Unroll the polysurface/solid
        unroller = rg.Unroller(j_brep)
        unroller.ExplodeOutput = False
        
        unrolled_results = unroller.PerformUnroll()
        if not unrolled_results or not unrolled_results[0]:
            continue
            
        u_breps = unrolled_results[0]
        path = GH_Path(i)
        
        for u_brep in u_breps:
            # REQUIREMENT 4: Array the geometry along the X-axis
            bbox = u_brep.GetBoundingBox(True)
            if not bbox.IsValid:
                continue
                
            width = bbox.Max.X - bbox.Min.X
            
            # Shift geometry to the current running X position and flatten to World XY origin
            shift_x = current_x - bbox.Min.X
            shift_y = -bbox.Min.Y
            xform = rg.Transform.Translation(shift_x, shift_y, 0)
            u_brep.Transform(xform)
            
            # REQUIREMENT 3: Split linework into cut and fold
            for edge in u_brep.Edges:
                crv = edge.ToNurbsCurve()
                
                # 'Naked' edges only belong to one face, meaning they are the outer cut boundaries
                if edge.Valence == rg.EdgeAdjacency.Naked:
                    cut_lines.Add(crv, path)
                    
                # 'Interior' edges are shared by two faces, making them the fold/hinge lines
                elif edge.Valence == rg.EdgeAdjacency.Interior:
                    fold_lines.Add(crv, path)
                    
            # Update the spacing tracker for the next cell's array position
            current_x += (width + space_val)