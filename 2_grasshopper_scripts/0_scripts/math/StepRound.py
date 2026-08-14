"""
Rounds a list of numbers to the nearest specified step value.

Inputs:
    values: List (The unrounded list of values)
    step: Float (Numeric step for rounding)

Outputs:
    stepped_values: List (The newly rounded values)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "StepRounding"
    ghenv.Component.NickName = "StepRound"
    ghenv.Component.Description = "Rounds a list of numbers to the nearest value of a given step."

    # --- Inputs Metadata ---
    # Index 0: values
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "values"
        ghenv.Component.Params.Input[0].NickName = "Vals"
        ghenv.Component.Params.Input[0].Description = "List (The unrounded list of values)"

    # Index 1: step
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "step"
        ghenv.Component.Params.Input[1].NickName = "Step"
        ghenv.Component.Params.Input[1].Description = "Float (Numeric step for rounding)"

    # --- Outputs Metadata ---
    # Index 0: stepped_values
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "stepped_values"
        ghenv.Component.Params.Output[0].NickName = "SteVa"
        ghenv.Component.Params.Output[0].Description = "List (The newly rounded values)"

except NameError:
    pass

# Initialize the output list
stepped_values = []

# Execute only if both inputs are provided
if values and step:
    for val in values:
        # Calculate the nearest step multiplier
        raw_rounded = round(val / step) * step

        # Clean up floating point precision artifacts (e.g., 0.350000000000001)
        # Rounding to 8 decimal places provides a clean output for Grasshopper
        clean_rounded = round(raw_rounded, 8)

        stepped_values.append(clean_rounded)