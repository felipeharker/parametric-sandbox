"""
Lists files in a directory.

Inputs:
    directory: String (item access, str)

Outputs:
    file_name: List of Strings (The names of the files in the directory)
"""

try:
    ghenv.Component.Name = "DirectoryFile"
    ghenv.Component.NickName = "DirFile"
    ghenv.Component.Description = "Lists files in a directory."
    ghenv.Component.Category = "CustomLib"
    ghenv.Component.SubCategory = "Document"
except NameError:
    pass

import os

if 'directory' in globals() and directory:
    file_name = os.listdir(directory)
else:
    file_name = []
