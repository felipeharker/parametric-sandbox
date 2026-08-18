"""
Remaps a list of values to a new target domain defined by user inputs.

Inputs:
    values: List of Numbers (The list of values to be remapped)
    value_a: Number (The start value of the target domain)
    value_b: Number (The end value of the target domain)

Outputs:
    remapped_values: List of Numbers (The remapped values)
"""

try:
    ghenv.Component.Name = "RemapValues"
    ghenv.Component.NickName = "ValRemap"
    ghenv.Component.Description = "Remaps a list of values to a new target domain defined by user inputs."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Math"
except NameError:
    pass

remapped_values = []

if values and value_a is not None and value_b is not None:
    min_val = min(values)
    max_val = max(values)
    
    orig_domain = max_val - min_val
    target_domain = value_b - value_a
    
    for val in values:
        if orig_domain == 0.0:
            remapped_values.append(value_a)
        else:
            mapped_val = value_a + (val - min_val) * (target_domain / orig_domain)
            remapped_values.append(mapped_val)