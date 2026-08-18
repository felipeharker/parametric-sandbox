"""
Programmatically packages a specified Grasshopper component into a custom User Object.

Inputs:
    target_nick: String (The nickname of the canvas node/cluster to package)
    obj_name: String (Display name of the new User Object)
    obj_desc: String (Tooltip description for the new User Object)
    category: String (Ribbon Tab name, e.g., "User")
    sub_category: String (Panel section name within the tab)
    icon_path: String (File path to a .png or bitmap image for the node icon)
    run: Boolean (Set to True to execute the creation)

Outputs:
    UserObject: String (Status message indicating success or failure)
"""

import Grasshopper as gh
import System.Drawing as drawing
import os

try:
    ghenv.Component.Name = "GenerateUserObj"
    ghenv.Component.NickName = "GenUserObj"
    ghenv.Component.Description = "Programmatically packages a specified Grasshopper component into a custom UserObject."
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
        "GenUserObj.py"
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
