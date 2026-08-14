"""
Lists files in a directory.

Inputs:
    directory: String (item access, str)

Outputs:
    file_name: List of Strings (The names of the files in the directory)
"""

try:
    # --- Component Metadata ---
    ghenv.Component.Name = "DirectoryFile"
    ghenv.Component.NickName = "DirFile"
    ghenv.Component.Description = "Lists files in a directory."

    # --- Inputs Metadata ---
    # Index 0: directory
    if ghenv.Component.Params.Input.Count > 0:
        ghenv.Component.Params.Input[0].Name = "directory"
        ghenv.Component.Params.Input[0].NickName = "Dire"
        ghenv.Component.Params.Input[0].Description = "String (item access, str)"

    # --- Outputs Metadata ---
    # Index 0: file_name
    if ghenv.Component.Params.Output.Count > 0:
        ghenv.Component.Params.Output[0].Name = "file_name"
        ghenv.Component.Params.Output[0].NickName = "FilNa"
        ghenv.Component.Params.Output[0].Description = "List of Strings (The names of the files in the directory)"

except NameError:
    pass

import os

if 'directory' in globals() and directory:
    file_name = os.listdir(directory)
else:
    file_name = []
