#! python 3
# category: CustomLib
# subcategory: Folding

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
import os

try:
    ghenv.Component.Name = "GridFoldPlanar"
    ghenv.Component.NickName = "GridFPlan"
    ghenv.Component.Description = "Creates folded 3D gridded geometries efficiently."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Folding"
    ghenv.Component.Message = ""
except NameError:
    pass


# 1. Resolve the path dynamically based on the Grasshopper file location
gh_doc = ghenv.Component.OnPingDocument()

if gh_doc and gh_doc.FilePath:
    gh_dir = os.path.dirname(gh_doc.FilePath)

    # Target your specific script
    script_path = os.path.join(
        gh_dir,
        "2_grasshopper_scripts",
        "0_scripts",
        "folding",
        "GridFPlan.py"
    )

    # 2. Execute the external code
    if os.path.exists(script_path):
        with open(script_path, 'r') as file:
            # exec() runs the script within the current namespace.
            # It will automatically pick up the inputs
            # and populate the outputs back into the component.
            exec(file.read(), globals(), locals())
    else:
        print(f"Error: Could not find script at {script_path}")
else:
    print("Warning: Please save the Grasshopper document first so relative paths work.")
