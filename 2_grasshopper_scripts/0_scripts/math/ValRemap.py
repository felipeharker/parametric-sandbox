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
    # --- Component Metadata ---
    ghenv.Component.Name = "RemapValues"
    ghenv.Component.NickName = "ValRemap"
    ghenv.Component.Description = "Remaps a list of values to a new target domain defined by user inputs."

    # --- Inputs Metadata ---
    # Index 0: values
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "values"
        ghenv.Component.Params.Input[0].NickName = "Vals"
        ghenv.Component.Params.Input[0].Description = "List of Numbers (The list of values to be remapped)"

    # Index 1: value_a
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "value_a"
        ghenv.Component.Params.Input[1].NickName = "Va"
        ghenv.Component.Params.Input[1].Description = "Number (The start value of the target domain)"

    # Index 2: value_b
    if ghenv.Component.Params.Input.Count > 2:
        ghenv.Component.Params.Input[2].Name = "value_b"
        ghenv.Component.Params.Input[2].NickName = "Vb"
        ghenv.Component.Params.Input[2].Description = "Number (The end value of the target domain)"

    # --- Outputs Metadata ---
    # Index 0: remapped_values
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "remapped_values"
        ghenv.Component.Params.Output[0].NickName = "Remap"
        ghenv.Component.Params.Output[0].Description = "List of Numbers (The remapped values)"

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