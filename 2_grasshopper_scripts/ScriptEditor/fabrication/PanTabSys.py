#! python 3
# category: CustomLib
# subcategory: Fabrication

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
import os

try:
    ghenv.Component.Name = "PanelTabSystem"
    ghenv.Component.NickName = "PanTab"
    ghenv.Component.Description = "Creates fold areas and tabs for an aluminum panel system based on a face boundary."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Fabrication"
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
        "fabrication",
        "PanTabSys.py"
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
