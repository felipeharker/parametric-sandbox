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
    ghenv.Component.Name = "RandomValueGenerator"
    ghenv.Component.NickName = "RandValGen"
    ghenv.Component.Description = "Generates a list of random float or integer numbers within a specified range."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Math"
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