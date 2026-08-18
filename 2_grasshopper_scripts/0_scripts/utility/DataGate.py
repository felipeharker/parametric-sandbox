"""
Utility to control the flow of data. Acts as a gate that can pass or block a data stream based on a boolean toggle.

Inputs:
    toggle: Boolean (Set to True to pass data, False to block data)
    data: Data/DataTree (The input data stream to be controlled)

Outputs:
    out_data: Data/DataTree (Outputs the original data if toggle is True, or an empty DataTree if False)
"""

try:
    ghenv.Component.Name = "DataGate"
    ghenv.Component.NickName = "DataGate"
    ghenv.Component.Description = "Acts as a gate to either pass data through or block it completely by outputting an empty DataTree."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Utility"
except NameError:
    pass

import Grasshopper as gh

# Check if the toggle is set to True
if toggle:
    # Pass the data through exactly as it is
    out_data = data
else:
    # Output an empty DataTree to block the stream completely
    out_data = gh.DataTree[object]()