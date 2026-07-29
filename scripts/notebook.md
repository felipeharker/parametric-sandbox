# scripts notebook

## description

this is the primary directory for all grasshopper script components' code

## agent goals

1. standardize and organize the code for each script- include the inputs and outputs as a comment at the top of the code. incldue access type (item, list, etc.) and type (int, float, crv, etc.)
2. standardize input and output names. capitalization, spacing, nicknames, and names should be standardized. if possible add a description for the input
3. standardize the component names, nicknames, and if possible add a description of the component as a tooltip.
4. in the ./scripts directory top level, write a summary for each script which explains what it does/how to use it


## enhancements

./grid-gen

a. please create individual grid generation .py scripts:

1. BoundRectGrid.py: rectangular grid in a boundary
2. BoundHexGrid.py: hexagonal grid in a boundary
3. BoundDiaGrid.py: this already exists, and the code/logic contained in this script should serve as a standard for the 2 new scripts.

## roadmap

there are some userobjects/clusters which i have saved and will eventually convert to python or c# script components. no action required on this section.