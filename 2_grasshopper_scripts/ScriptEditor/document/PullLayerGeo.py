"""
Pulls geometry from a specified Rhino layer or sublayer.

Inputs:
    layer_name: Text (item access, str)
    pull: Boolean (item access, bool)

Outputs:
    geo: List of Geometry (The geometry pulled from the specified layer)
"""

import Rhino
import os

try:
    ghenv.Component.Name = "PullLayerGeometry"
    ghenv.Component.NickName = "PullLayerGeo"
    ghenv.Component.Description = "Pulls geometry from a specified Rhino layer or sublayer."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Document"
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
        "document",
        "PullLayerGeo.py"
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
