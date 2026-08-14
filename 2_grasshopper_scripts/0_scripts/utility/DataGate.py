"""
Utility to control the flow of data. Acts as a gate that can pass or block a data stream based on a boolean toggle.

Inputs:
    toggle: Boolean (Set to True to pass data, False to block data)
    data: Data/DataTree (The input data stream to be controlled)

Outputs:
    out_data: Data/DataTree (Outputs the original data if toggle is True, or an empty DataTree if False)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "DataGate"
    ghenv.Component.NickName = "DataGate"
    ghenv.Component.Description = "Acts as a gate to either pass data through or block it completely by outputting an empty DataTree."

    # --- Inputs Metadata ---
    # Index 0: toggle
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "toggle"
        ghenv.Component.Params.Input[0].NickName = "Tog"
        ghenv.Component.Params.Input[0].Description = "Boolean (Set to True to pass data, False to block data)"

    # Index 1: data
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "data"
        ghenv.Component.Params.Input[1].NickName = "Data"
        ghenv.Component.Params.Input[1].Description = "Data/DataTree (The input data stream to be controlled)"

    # --- Outputs Metadata ---
    # Index 0: out_data
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "out_data"
        ghenv.Component.Params.Output[0].NickName = "Out"
        ghenv.Component.Params.Output[0].Description = "Data/DataTree (Outputs the original data if toggle is True, or an empty DataTree if False)"

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