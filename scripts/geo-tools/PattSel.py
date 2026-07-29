import itertools

# 1. Generate all possible 7-bit combinations
all_combinations = list(itertools.product([0, 1], repeat=7))

# 2. Filter to keep only those with at least two 1s
valid_combinations = [comb for comb in all_combinations if sum(comb) >= 2]

# 3. Output the selected combination based on the input index
if Index is not None:
    # Ensure the index stays within the valid range (0-119)
    safe_index = max(0, min(int(Index), len(valid_combinations) - 1))
    
    # Assign the combination to the output variable as a list
    # Grasshopper will automatically output this as 7 distinct items
    Values = list(valid_combinations[safe_index])
else:
    Values = []