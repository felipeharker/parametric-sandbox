"""
Selects a 7-bit combination pattern based on an index.

Inputs:
    index: Number (item access, int)

Outputs:
    values: List of Numbers (The selected 7-bit combination pattern)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "PatternSelector"
    ghenv.Component.NickName = "PattSel"
    ghenv.Component.Description = "Selects a 7-bit combination pattern based on an index."

    # --- Inputs Metadata ---
    # Index 0: index
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "index"
        ghenv.Component.Params.Input[0].NickName = "Idx"
        ghenv.Component.Params.Input[0].Description = "Number (item access, int)"

    # --- Outputs Metadata ---
    # Index 0: values
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "values"
        ghenv.Component.Params.Output[0].NickName = "Vals"
        ghenv.Component.Params.Output[0].Description = "List of Numbers (The selected 7-bit combination pattern)"

except NameError:
    pass

import itertools

all_combinations = list(itertools.product([0, 1], repeat=7))
valid_combinations = [comb for comb in all_combinations if sum(comb) >= 2]

if 'index' in globals() and index is not None:
    safe_index = max(0, min(int(index), len(valid_combinations) - 1))
    values = list(valid_combinations[safe_index])
else:
    values = []
