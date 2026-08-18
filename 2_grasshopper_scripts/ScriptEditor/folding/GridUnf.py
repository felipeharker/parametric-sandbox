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
import os

try:
    ghenv.Component.Name = "GridUnfold"
    ghenv.Component.NickName = "GridUnf"
    ghenv.Component.Description = "Unrolls 3D folded geometries into 2D cut and fold linework for fabrication."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Folding"
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
        "GridUnf.py"
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
