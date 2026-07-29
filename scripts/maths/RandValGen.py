# --- Grasshopper Python Component ---
# Description: Generates a list of random float numbers within a specified range.

# Input definitions in Grasshopper:
# count: Integer (Number of random values to generate)
# min_val: Number (Minimum random value)
# max_val: Number (Maximum random value)
# seed: Integer (Randomness seed for reproducible results)

# Output definitions in Grasshopper:
# values: List of Numbers (The generated random float values)

import random

def generate_random_floats(num_count, minimum, maximum, rand_seed):
    # Pre-checks
    if num_count is None or num_count <= 0:
        return []
    if minimum is None or maximum is None:
        return []
        
    # Initialize the random number generator with the provided seed
    if rand_seed is not None:
        random.seed(rand_seed)
        
    # Ensure min and max are properly ordered just in case inputs are swapped
    actual_min = min(minimum, maximum)
    actual_max = max(minimum, maximum)
    
    generated_values = []
    
    # Generate the random floats
    for _ in range(int(num_count)):
        # random.uniform(a, b) generates a random float N such that a <= N <= b
        val = random.uniform(actual_min, actual_max)
        generated_values.append(val)
        
    return generated_values

# --- GH Python component execution ---
# Ensure your output parameter on the component is renamed to 'values'

values = generate_random_floats(count, min_val, max_val, seed)