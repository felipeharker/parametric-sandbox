#! python 3
# category: CustomLib
# subcategory: Utility

"""
Utility to control the flow of data. Acts as a gate that can pass or block a data stream based on a boolean toggle.

Inputs:
    toggle: Boolean (Set to True to pass data, False to block data)
    data: Data/DataTree (The input data stream to be controlled)

Outputs:
    out_data: Data/DataTree (Outputs the original data if toggle is True, or an empty DataTree if False)
"""

import Grasshopper as gh
import os

try:
    ghenv.Component.Name = "DataGate"
    ghenv.Component.NickName = "DataGate"
    ghenv.Component.Description = "Acts as a gate to either pass data through or block it completely by outputting an empty DataTree."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Utility"
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
        "utility",
        "DataGate.py"
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
