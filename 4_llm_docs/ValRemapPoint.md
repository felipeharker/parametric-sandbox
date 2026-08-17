# Value Remap, Point

## Objectives:

Remap the value of a list based on point distances from a given point. this means the user will have 4 inputs described below

## Inputs:

attractor
points
value_a
value_b

## Outputs:

remapped_values

## Model Notes:

Sometimes, it can be challenging to describe verbally how a design/workflow should function and what the desired outcome is. if anything, no matter how small or large, is unclear, ambigious, or unspecified, ALWAYS ask for clarification instead of making assumptions and potentially outputting buggy code.

## Code and Output Notes:

Below is a standard codeblock which should be placed above all created scripts. the information contained within it should reflect the script's contents. The code below should serve as a standard/example only.

Adhere strictly to written standards like spacing, capitalization, etc. 

Adhere strictly to naming conventions for the component, the component nickname, input naming, and output naming.

Adhere stricly to the standard for commenting information about the script's inputs/outputs and their input details so I can configure the component easily.

/// CODE BELOW ///

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
/// END ///