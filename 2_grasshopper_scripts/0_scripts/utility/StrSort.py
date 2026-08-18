"""
Sorts a list of strings using Natural Sorting (e.g., 2 comes before 10).

Inputs:
    values: List of Strings (list access, str)

Outputs:
    sorted_values: List of Strings (The naturally sorted list)
"""

try:
    ghenv.Component.Name = "StringSort"
    ghenv.Component.NickName = "StrSort"
    ghenv.Component.Description = "Sorts a list of strings using Natural Sorting."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Utility"
except NameError:
    pass

import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]

if 'values' in globals() and values:
    sorted_values = sorted(values, key=natural_sort_key)
else:
    sorted_values = []
