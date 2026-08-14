"""
Generates a list of random numbers (float or integer) within a specified range.

Inputs:
    count: Integer (Number of random values to generate)
    min_val: Number (Minimum random value)
    max_val: Number (Maximum random value)
    as_int: Boolean (0 = float, 1 = integer)
    seed: Integer (Randomness seed for reproducible results)

Outputs:
    values: List of Numbers (The generated random values)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "RandomValueGenerator"
    ghenv.Component.NickName = "RandValGen"
    ghenv.Component.Description = "Generates a list of random float or integer numbers within a specified range."

    # --- Inputs Metadata ---
    # Index 0: count
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "count"
        ghenv.Component.Params.Input[0].NickName = "Cnt"
        ghenv.Component.Params.Input[0].Description = "Integer (Number of random values to generate)"

    # Index 1: min_val
    if ghenv.Component.Params.Input.Count > 1:
        ghenv.Component.Params.Input[1].Name = "min_val"
        ghenv.Component.Params.Input[1].NickName = "Min"
        ghenv.Component.Params.Input[1].Description = "Number (Minimum random value)"

    # Index 2: max_val
    if ghenv.Component.Params.Input.Count > 2:
        ghenv.Component.Params.Input[2].Name = "max_val"
        ghenv.Component.Params.Input[2].NickName = "Max"
        ghenv.Component.Params.Input[2].Description = "Number (Maximum random value)"

    # Index 3: as_int
    if ghenv.Component.Params.Input.Count > 3:
        ghenv.Component.Params.Input[3].Name = "as_int"
        ghenv.Component.Params.Input[3].NickName = "AsIn"
        ghenv.Component.Params.Input[3].Description = "Boolean (0 = float, 1 = integer)"

    # Index 4: seed
    if ghenv.Component.Params.Input.Count > 4:
        ghenv.Component.Params.Input[4].Name = "seed"
        ghenv.Component.Params.Input[4].NickName = "Seed"
        ghenv.Component.Params.Input[4].Description = "Integer (Randomness seed for reproducible results)"

    # --- Outputs Metadata ---
    # Index 0: values
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "values"
        ghenv.Component.Params.Output[0].NickName = "Vals"
        ghenv.Component.Params.Output[0].Description = "List of Numbers (The generated random values)"

except NameError:
    pass

import random

def generate_random_values(num_count, minimum, maximum, as_integer, rand_seed):
    if num_count is None or num_count <= 0:
        return []
    if minimum is None or maximum is None:
        return []

    if rand_seed is not None:
        random.seed(rand_seed)

    actual_min = min(minimum, maximum)
    actual_max = max(minimum, maximum)

    generated_values = []

    for _ in range(int(num_count)):
        if as_integer:
            # Casts the limits to integers and generates an inclusive integer
            val = random.randint(int(actual_min), int(actual_max))
        else:
            # Generates a float
            val = random.uniform(actual_min, actual_max)

        generated_values.append(val)

    return generated_values

if 'count' in globals() and 'min_val' in globals() and 'max_val' in globals():
    seed_val = seed if 'seed' in globals() else None
    as_int_val = as_int if 'as_int' in globals() else False
    values = generate_random_values(count, min_val, max_val, as_int_val, seed_val)