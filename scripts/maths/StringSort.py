"""
Sorts a list of strings using Natural Sorting (e.g., 2 comes before 10).
Inputs:
    x: The list of items to sort (Set access to 'List', Type hint 'String')
Outputs:
    a: The naturally sorted list
"""
import re

def natural_sort_key(s):
    # This splits the string into text and numbers
    # e.g. "img (100).png" -> ["img (", 100, ").png"]
    # It converts the digits into actual integers so they sort correctly.
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]

if x:
    # Sort the list using our custom natural sorting rule
    a = sorted(x, key=natural_sort_key)
else:
    a = []