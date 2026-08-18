"""
Creates parametric tab perforations within a frame boundary for an aluminum panel system.

Inputs:
    boundary: Geometry (item access, crv)
    tab_height: Number (item access, float)
    tab_width: Number (item access, float)
    tab_space_x: Number (item access, float)
    tab_space_y: Number (item access, float)

Outputs:
    frame_face: Curve (The original rectangular frame face)
    tabs: List of Curves (The curves representing the newly created tabs/openings)
"""

import Rhino.Geometry as rg
import os

try:
    ghenv.Component.Name = "FrameTabSystem"
    ghenv.Component.NickName = "FrmTab"
    ghenv.Component.Description = "Creates parametric tab perforations within a frame boundary for an aluminum panel system."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Fabrication"
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
        "FrameTabSys.py"
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
