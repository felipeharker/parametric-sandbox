# Grasshopper Scripts Overview

This directory contains standard Python and C# script components used for various Grasshopper workflows.

## doc-configs
- **DirectoryFile.py**: Lists all files within a specified directory.
- **ParamController1.py**: Updates Grasshopper parameters in the active document from a given CSV file, matching `input name`, `type`, and `value`.
- **ParamController2.py**: Similar to ParamController1, but supports an optional section filter to only update specific parameter groups.
- **ParamExporter.py**: Exports top-level disconnected Grasshopper parameters and their current values to a CSV file.

## geo-tools
- **ImageHue.py**: Calculates the luminance/hue values of an image mapped over a set of provided 2D points.
- **PattSel.py**: Given an index, selects a valid 7-bit combination pattern that contains at least two `1`s.

## grid-gen
- **BoundDiaGrid.py**: Creates a grid of individual closed diamond cells within a region.
- **BoundHexGrid.py**: Creates a grid of individual closed hexagonal cells within a region.
- **BoundRectGrid.py**: Creates a grid of individual closed rectangular cells within a region.
- **BoundPanel.py**: Creates a grid of rectangular panels that perfectly fit within a bounding curve, capping the ends uniformly.

## maths
- **RandValGen.py**: Generates a list of random float numbers within a specified minimum and maximum range based on a seed.
- **StringSort.py**: Sorts a list of strings using Natural Sorting (e.g., ensuring '2' comes before '10').

## misc
- **ClusterCrack.cs**: A C# component for bypassing cluster passwords or un-locking clusters.
