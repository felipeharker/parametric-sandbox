"""
Selects a 7-bit combination pattern based on an index.

Inputs:
    index: Number (item access, int)

Outputs:
    values: List of Numbers (The selected 7-bit combination pattern)
"""

try:
    ghenv.Component.Name = "PatternSelector"
    ghenv.Component.NickName = "PSel"
    ghenv.Component.Description = "Selects a 7-bit combination pattern based on an index."
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
