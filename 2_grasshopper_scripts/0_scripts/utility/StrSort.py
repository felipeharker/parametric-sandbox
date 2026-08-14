"""
Sorts a list of strings using Natural Sorting (e.g., 2 comes before 10).

Inputs:
    values: List of Strings (list access, str)

Outputs:
    sorted_values: List of Strings (The naturally sorted list)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "StringSort"
    ghenv.Component.NickName = "StrSort"
    ghenv.Component.Description = "Sorts a list of strings using Natural Sorting."

    # --- Inputs Metadata ---
    # Index 0: values
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "values"
        ghenv.Component.Params.Input[0].NickName = "Vals"
        ghenv.Component.Params.Input[0].Description = "List of Strings (list access, str)"

    # --- Outputs Metadata ---
    # Index 0: sorted_values
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "sorted_values"
        ghenv.Component.Params.Output[0].NickName = "Sort"
        ghenv.Component.Params.Output[0].Description = "List of Strings (The naturally sorted list)"

except NameError:
    pass

import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]

if 'values' in globals() and values:
    sorted_values = sorted(values, key=natural_sort_key)
else:
    sorted_values = []
