#! python 3
# category: CustomLib
# subcategory: Document

"""
Updates Grasshopper parameters from a CSV file.

Inputs:
    update: Boolean (item access, bool)
    csv_file: String (item access, str)

Outputs:
    (None)
"""

import os
import csv
import Grasshopper as gh
import System

try:
    ghenv.Component.Name = "ParamController1"
    ghenv.Component.NickName = "ParamCont1"
    ghenv.Component.Description = "Updates Grasshopper parameters from a CSV file."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Document"
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
        "document",
        "ParamCont1.py"
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
