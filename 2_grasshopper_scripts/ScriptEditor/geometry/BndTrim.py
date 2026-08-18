"""
Utility to trim curves with a region, closing the curves along the intersection boundary if they were originally closed.

Inputs:
    curves: List of Curves (The open or closed curves to be trimmed)
    region: Curve (The closed boundary region to trim the curves against)

Outputs:
    trimmed_curves: List of Curves (The resulting trimmed and appropriately closed curves)
"""

import Rhino.Geometry as rg
import scriptcontext as sc
import os

try:
    ghenv.Component.Name = "BoundTrim"
    ghenv.Component.NickName = "BndTrim"
    ghenv.Component.Description = "Utility to trim curves with a region, closing the curves along the intersection boundary if they were originally closed."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Geometry"
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
        "geometry",
        "BndTrim.py"
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
