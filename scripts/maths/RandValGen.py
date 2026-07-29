"""
Generates a list of random float numbers within a specified range.

Inputs:
    count: Integer (Number of random values to generate)
    min_val: Number (Minimum random value)
    max_val: Number (Maximum random value)
    seed: Integer (Randomness seed for reproducible results)

Outputs:
    values: List of Numbers (The generated random float values)
"""

try:
    ghenv.Component.Name = "RandomValueGenerator"
    ghenv.Component.NickName = "RandValGen"
    ghenv.Component.Description = "Generates a list of random float numbers within a specified range."
except NameError:
    pass

import random

def generate_random_floats(num_count, minimum, maximum, rand_seed):
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
        val = random.uniform(actual_min, actual_max)
        generated_values.append(val)
        
    return generated_values

if 'count' in globals() and 'min_val' in globals() and 'max_val' in globals():
    seed_val = seed if 'seed' in globals() else None
    values = generate_random_floats(count, min_val, max_val, seed_val)
